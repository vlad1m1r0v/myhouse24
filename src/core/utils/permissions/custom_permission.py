from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import logout

from src.core.utils import is_ajax


class CustomPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = None
    permission_denied_message = 'У Вас немає доступу до цієї сторінки'

    def handle_no_permission(self):
        if is_ajax(self.request):
            return JsonResponse(
                status=403,
                data={'success': False, 'message': self.permission_denied_message}
            )

        messages.error(self.request, self.permission_denied_message)
        logout(self.request)
        return redirect(reverse('authentication:adminlte:login'))

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_anonymous \
                or not self.request.user.status == 'active' \
                or not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(self.request, *args, **kwargs)
