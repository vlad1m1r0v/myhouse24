from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from src.flats.models import Flat
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
                formset.save()

                messages.success(self.request, "Квитанцію успішно створено")

            except Exception as e:
                messages.error(self.request, f"Виникла помилка при збереженні квитанції: {e}")

        return redirect('adminlte:receipts:create')
