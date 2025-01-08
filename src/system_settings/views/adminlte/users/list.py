from django.views.generic import TemplateView

from .mixin import UserPermissionRequiredMixin


class AdminUsersView(UserPermissionRequiredMixin,
                     TemplateView):
    template_name = 'system_settings/adminlte/users/list.html'