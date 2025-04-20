from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView

from src.authentication.models import CustomUser
from src.system_settings.tasks import send_password_update_notification
from .mixin import (
    FlatOwnerPermissionRequiredMixin,
    HouseUserRequiredMixin
)
from ...forms import AdminFlatOwnerForm


class AdminFlatOwnerUpdateView(SuccessMessageMixin,
                               HouseUserRequiredMixin,
                               FlatOwnerPermissionRequiredMixin,
                               UpdateView):
    model = CustomUser
    template_name = 'flat_owners/adminlte/update.html'
    form_class = AdminFlatOwnerForm
    success_url = reverse_lazy('adminlte:flat-owners:list')
    success_message = 'Дані власника квартири успішно оновлено'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Дані користувача успішно оновлено")

        password = form.cleaned_data.get('new_password')
        email = form.cleaned_data.get('email')

        login_path = reverse('authentication:account:login')
        login_url = self.request.build_absolute_uri(login_path)

        if password:
            send_password_update_notification.delay(
                subject_template_name='system_settings/adminlte/users/password_change_subject.txt',
                email_template_name='system_settings/adminlte/users/password_change_notification.html',
                context={
                    'email': email,
                    'password': password,
                    'login_url': login_url,
                },
                from_email=settings.EMAIL_HOST_USER,
                to_email=email
            )

        return response


    def form_invalid(self, form):
        messages.error(self.request, "Помилка при оновленні данних користувача")
        return super().form_invalid(form)