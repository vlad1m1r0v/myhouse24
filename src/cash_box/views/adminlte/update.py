from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .mixin import (
    CashBoxPermissionRequiredMixin,
    HouseUserRequiredMixin
)
from ...forms import AdminTransactionForm
from ...models import Transaction


class AdminTransactionUpdateView(
    SuccessMessageMixin,
    HouseUserRequiredMixin,
    CashBoxPermissionRequiredMixin,
    UpdateView):
    success_message = 'Транзакцію успішно оновлено'
    success_url = reverse_lazy('adminlte:cash-box:list')
    model = Transaction
    form_class = AdminTransactionForm
    template_name = 'cash_box/adminlte/update.html'

    def get_queryset(self):
        return super().get_queryset().select_related('owner', 'payment_item', 'personal_account', 'manager')
