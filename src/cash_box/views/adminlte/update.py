from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .mixin import CashBoxPermissionRequiredMixin
from ...forms import AdminTransactionForm
from ...models import Transaction


class AdminTransactionUpdateView(
    SuccessMessageMixin,
    CashBoxPermissionRequiredMixin,
    UpdateView):
    success_message = 'Транзакцію успішно оновлено'
    # TODO: change to cash box list page
    success_url = reverse_lazy('adminlte:cash-box:create')
    model = Transaction
    form_class = AdminTransactionForm
    template_name = 'cash_box/adminlte/update.html'