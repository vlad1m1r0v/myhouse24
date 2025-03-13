from django.contrib.messages.context_processors import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import View

from src.core.utils import is_ajax
from ...models import Transaction
from .mixin import (
    HouseUserRequiredMixin,
    CashBoxPermissionRequiredMixin
)


class AdminTransactionDeleteView(
    HouseUserRequiredMixin,
    CashBoxPermissionRequiredMixin,
    View
):
    def post(self, *args, **kwargs):
        transaction_id = self.kwargs.get('pk')
        Transaction.objects.filter(id=transaction_id).delete()

        if is_ajax(self.request):
            return JsonResponse({'success': True})

        else:
            messages.success(self.request, 'Транзакцію успішно видалено')
            return redirect(reverse_lazy('adminlte:cash-box:list'))
