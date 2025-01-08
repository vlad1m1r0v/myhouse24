from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from src.authentication.models import CustomUser
from src.system_settings.forms import AdminUserForm
from .mixin import UserPermissionRequiredMixin


class AdminUserCreateView(SuccessMessageMixin,
                          UserPermissionRequiredMixin,
                          CreateView):
    model = CustomUser
    template_name = 'system_settings/adminlte/users/create.html'
    form_class = AdminUserForm
    success_url = reverse_lazy('adminlte:system-settings:users:list')
    success_message = 'Новий користувач успішно створений'