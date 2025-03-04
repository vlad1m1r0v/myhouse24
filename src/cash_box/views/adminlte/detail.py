from django.views.generic import DetailView

from .mixin import (
    CashBoxPermissionRequiredMixin,
    HouseUserRequiredMixin
)

from ...models import Transaction


class AdminTransactionDetailView(
    HouseUserRequiredMixin,
    CashBoxPermissionRequiredMixin,
    DetailView):
    model = Transaction
    template_name = 'cash_box/adminlte/detail.html'
    context_object_name = 'transaction'

    def get_queryset(self):
        return super().get_queryset().select_related('owner', 'personal_account', 'payment_item', 'manager')