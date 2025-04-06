from django.contrib.auth import logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy

from src.core.utils import is_ajax


class OwnerRequiredMixin(UserPassesTestMixin):
    permission_denied_message = "Не вдалось увійти в особистий кабінет користувача"
    login_url = 'authentication:account:login'

    def test_func(self):
        user = self.request.user
        return all([
            user.is_authenticated,
            not user.is_staff,
            not user.is_superuser,
            user.is_active,
            user.status == 'active'
        ])

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            logout(self.request)

        if is_ajax(self.request):
            return JsonResponse(
                status=403,
                data={'success': False, 'message': self.permission_denied_message}
            )
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse_lazy(self.login_url))