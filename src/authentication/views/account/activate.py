from django.contrib import messages
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View

from src.authentication.models import CustomUser
from src.authentication.tokens import account_activation_token


class AccountActivateView(View):
    def get(self, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(self.request, "Ваш акаунт підтверджено")
            return redirect('authentication:account:login')
        else:
            messages.error(self.request, "Недійсне посилання для підтвердження акаунту")

        return redirect('authentication:account:register')