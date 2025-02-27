from datetime import datetime

from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import TemplateView

from src.meter_indicators.models import (
    MeterIndicator,
    StatusChoices
)
from .mixin import ReceiptsPermissionRequiredMixin
from ...forms import (
    AdminReceiptForm,
    AdminReceiptServiceFormSet
)


class AdminReceiptsCreateView(
    ReceiptsPermissionRequiredMixin,
    TemplateView
):
    template_name = 'payment_receipts/adminlte/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = AdminReceiptForm()
        context['formset'] = AdminReceiptServiceFormSet()

        return context

    def post(self, *args, **kwargs):
        form = AdminReceiptForm(self.request.POST)
        formset = AdminReceiptServiceFormSet(self.request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    receipt = form.save()

                    services = formset.save(commit=False)
                    for service in services:
                        service.receipt = receipt
                        service.save()

                        if not service.meter_indicator:
                            meter_indicator = MeterIndicator.objects.create(
                                no=datetime.now().timestamp() * 1000,
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
