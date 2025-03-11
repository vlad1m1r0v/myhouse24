from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .mixin import CashBoxPermissionRequiredMixin
from ...forms import AdminTransactionForm
from ...models import Transaction


class AdminTransactionCreateView(
    SuccessMessageMixin,
    CashBoxPermissionRequiredMixin,
    CreateView):
    success_message = 'Транзакцію успішно створено'
    success_url = reverse_lazy('adminlte:cash-box:list')
    model = Transaction
    form_class = AdminTransactionForm
    template_name = 'cash_box/adminlte/create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        transaction_id = self.request.GET.get('transaction_id')
        transaction_type = self.request.GET.get('type')

        if transaction_type:
            kwargs['initial'] = {'type': transaction_type}

        if transaction_id:
            transaction = get_object_or_404(Transaction, id=transaction_id)
            kwargs['initial'] = {
                'no': transaction.no,
                'date': transaction.date,
                'type': transaction.type,
                'owner': transaction.owner,
                'personal_account': transaction.personal_account,
                'payment_item': transaction.payment_item,
                'amount': transaction.amount,
                'is_complete': transaction.is_complete,
                'manager': transaction.manager,
                'comment': transaction.comment,
            }

        return kwargs
