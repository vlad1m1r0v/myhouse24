from django.views.generic import TemplateView

from .mixin import UserPermissionRequiredMixin


class AdminUsersView(UserPermissionRequiredMixin,
                     TemplateView):
    template_name = 'adminlte/system_settings/users/list.html'