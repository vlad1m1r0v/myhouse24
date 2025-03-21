from django.views.generic import FormView

from src.cash_box.forms import AdminCashBoxFiltersForm
from src.dashboard.views.adminlte.mixin import AdminBalanceMixin
from src.personal_accounts.models import PersonalAccount

from .mixin import CashBoxPermissionRequiredMixin

class AdminCashBoxListView(
    AdminBalanceMixin,
    CashBoxPermissionRequiredMixin,
    FormView
):
    template_name = 'cash_box/adminlte/list.html'
    form_class = AdminCashBoxFiltersForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = context.pop('form')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        initial = {}

        account_id = self.request.GET.get('account_id')
        transaction_type = self.request.GET.get('type')

        if transaction_type:
            initial['type'] = transaction_type

        if account_id:
            account = PersonalAccount.objects.get(id=account_id)
            initial['personal_account'] = account.no

        kwargs['initial'] = initial
        return kwargs
