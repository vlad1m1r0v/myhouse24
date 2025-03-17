from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from src.flat_owners.forms import AdminFlatOwnersInvitationForm
from src.system_settings.tasks import send_invitation_email

from .mixin import FlatOwnerPermissionRequiredMixin


class AdminFlatOwnersInviteView(FlatOwnerPermissionRequiredMixin,
                                FormView):
    form_class = AdminFlatOwnersInvitationForm
    template_name = 'flat_owners/adminlte/invite.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        # TODO: change to account login url
        login_path = reverse('authentication:adminlte:login')
        login_url = self.request.build_absolute_uri(login_path)

        send_invitation_email.delay(email, login_url)

        messages.success(self.request, 'Запрошення успішно надіслано')

        return redirect(reverse('adminlte:flat-owners:list'))
