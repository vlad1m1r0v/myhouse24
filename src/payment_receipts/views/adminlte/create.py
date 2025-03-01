from datetime import datetime

from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import TemplateView

from src.flats.models import Flat
from src.meter_indicators.models import (
    MeterIndicator,
    StatusChoices
)
from .mixin import ReceiptsPermissionRequiredMixin
from ...forms import (
    AdminReceiptForm,
    AdminReceiptServiceFormSet
)
from ...models import Receipt


class AdminReceiptsCreateView(
    ReceiptsPermissionRequiredMixin,
    TemplateView
):
    template_name = 'payment_receipts/adminlte/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        flat_id = self.request.GET.get('flat_id')
        receipt_id = self.request.GET.get('receipt_id')

        if flat_id:
            flat = Flat.objects.select_related('house', 'section').get(id=flat_id)

            context['form'] = AdminReceiptForm(
                self.request.POST or None,
                initial={
                    'house': flat.house,
                    'section': flat.section,
                    'flat': flat
                })
            context['formset'] = AdminReceiptServiceFormSet()

        elif receipt_id:
            receipt = Receipt.objects.get(id=receipt_id)

            context['form'] = AdminReceiptForm(
                self.request.POST or None,
                initial={
                    'house': receipt.house,
                    'section': receipt.section,
                    'flat': receipt.flat
                },
                instance=receipt
            )

            context['formset'] = AdminReceiptServiceFormSet(instance=receipt)

        else:
            context['form'] = AdminReceiptForm()
            context['formset'] = AdminReceiptServiceFormSet()

        return context

    def post(self, *args, **kwargs):
        form = AdminReceiptForm(self.request.POST)
        formset = AdminReceiptServiceFormSet(self.request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                receipt = form.save()
                formset.instance = receipt
                services = formset.save(commit=False)

                for service in services:
                    service.receipt = receipt
                    service.save()

                    if not service.meter_indicator:
                        meter_indicator = MeterIndicator.objects.create(
                            no=int(datetime.now().timestamp() * 1000),
                            date=receipt.date,
                            status=StatusChoices.ACCOUNTED,
                            house=receipt.house,
                            section=receipt.section,
                            flat=receipt.flat,
                            service=service.service,
                            value=service.value
                        )
                        service.meter_indicator = meter_indicator
                        service.save()

                    else:
                        service.meter_indicator.value = service.value
                        service.meter_indicator.status = StatusChoices.ACCOUNTED
                        service.meter_indicator.save()

                    messages.success(self.request, "Квитанцію успішно створено")

            except Exception as e:
                messages.error(self.request, f"Виникла помилка при збереженні квитанції: {e}")

        return redirect('adminlte:receipts:create')
