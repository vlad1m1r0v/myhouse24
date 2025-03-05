from django.views.generic import TemplateView

from src.cash_box.forms import AdminCashBoxFiltersForm
from src.cash_box.views.adminlte.mixin import CashBoxPermissionRequiredMixin


class AdminCashBoxListView(
    CashBoxPermissionRequiredMixin,
    TemplateView
):
    template_name = 'cash_box/adminlte/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filters'] = AdminCashBoxFiltersForm()

        return context
