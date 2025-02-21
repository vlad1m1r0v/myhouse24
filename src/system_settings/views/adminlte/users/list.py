from django.views.generic import TemplateView

from src.system_settings.forms import AdminUsersFiltersForm
from .mixin import UserPermissionRequiredMixin


class AdminUsersView(UserPermissionRequiredMixin,
                     TemplateView):
    template_name = 'system_settings/adminlte/users/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filters'] = AdminUsersFiltersForm()

        return context