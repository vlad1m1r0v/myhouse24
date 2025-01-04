from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from src.authentication.models import CustomUser
from src.system_settings.forms import AdminUserForm
from .mixin import UserPermissionRequiredMixin


class AdminUserUpdateView(SuccessMessageMixin,
                          UserPermissionRequiredMixin,
                          UpdateView):
    model = CustomUser
    form_class = AdminUserForm
    template_name = 'adminlte/system_settings/users/update.html'
    success_url = reverse_lazy('adminlte:system-settings:users:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Дані користувача успішно оновлено")

        if form.instance == self.request.user:
            update_session_auth_hash(self.request, form.instance)

        return response

    def form_invalid(self, form):
        messages.error(self.request, "Помилка при оновленні данних користувача")
        return super().form_invalid(form)