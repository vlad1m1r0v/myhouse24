from django.views.generic import TemplateView

from .mixin import PersonalAccountPermissionRequiredMixin
from ...forms import AdminPersonalAccountsFiltersForm


class AdminPersonalAccountsListView(
    PersonalAccountPermissionRequiredMixin,
    TemplateView
):
    template_name = 'personal_accounts/adminlte/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filters'] = AdminPersonalAccountsFiltersForm()

        return context