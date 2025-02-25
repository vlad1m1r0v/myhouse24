from django.views.generic import TemplateView

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
