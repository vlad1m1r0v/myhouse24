from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from ...models import Transaction
from .mixin import (
    HouseUserRequiredMixin,
    CashBoxPermissionRequiredMixin
)


class AdminTransactionDeleteView(
    SuccessMessageMixin,
    HouseUserRequiredMixin,
    CashBoxPermissionRequiredMixin,
    DeleteView
):
    model = Transaction
    success_message = 'Транзакцію успішно видалено'
    success_url = reverse_lazy('adminlte:cash-box:list')
