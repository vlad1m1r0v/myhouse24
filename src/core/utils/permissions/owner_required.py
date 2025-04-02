from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy

from src.core.utils import is_ajax


class OwnerRequiredMixin(UserPassesTestMixin):
    permission_denied_message = "Користувач не увійшов в систему або не є власником квартири"
    login_url = 'authentication:account:login'

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and not user.is_staff and not user.is_superuser

    def handle_no_permission(self):
        if is_ajax(self.request):
            return JsonResponse(
                status=403,
                data={'success': False, 'message': self.permission_denied_message}
            )
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse_lazy(self.login_url))