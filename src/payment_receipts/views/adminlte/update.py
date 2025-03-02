from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .mixin import (
    ReceiptsPermissionRequiredMixin,
    HouseUserRequiredMixin
)
from ...forms import (
    AdminReceiptForm,
    AdminReceiptServiceFormSet
)
from ...models import Receipt


class AdminReceiptsUpdateView(
    HouseUserRequiredMixin,
    ReceiptsPermissionRequiredMixin,
    TemplateView
):
    template_name = 'payment_receipts/adminlte/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        receipt = Receipt.objects.prefetch_related('services').get(pk=self.kwargs['pk'])

        context['form'] = AdminReceiptForm(instance=receipt)
        context['formset'] = AdminReceiptServiceFormSet(
            instance=receipt,
            queryset=receipt.services.all()
        )

        return context

    def post(self, *args, **kwargs):
        instance = Receipt.objects.get(pk=self.kwargs['pk'])
        form = AdminReceiptForm(self.request.POST, instance=instance)
        formset = AdminReceiptServiceFormSet(self.request.POST, instance=instance)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(self.request, "Квитанцію успішно оновлено")

        return redirect('adminlte:receipts:create')
