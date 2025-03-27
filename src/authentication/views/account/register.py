from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView

from src.authentication.forms import AccountRegisterForm
from src.authentication.models import CustomUser
from src.authentication.tasks import send_verification_email
from src.authentication.tokens import account_activation_token


class AccountRegisterView(
    SuccessMessageMixin,
    CreateView
):
    model = CustomUser
    form_class = AccountRegisterForm
    template_name = 'authentication/account/register.html'
    success_message = 'Вам відправлено лист підтвердження на пошту'
    success_url = reverse_lazy('authentication:account:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        domain = get_current_site(self.request).domain
        uid = urlsafe_base64_encode(force_bytes(self.object.pk))
        token = account_activation_token.make_token(self.object)
        protocol = 'https' if self.request.is_secure() else 'http'
        email = self.object.email

        send_verification_email.delay(domain, uid, token, protocol, email)

        return response
