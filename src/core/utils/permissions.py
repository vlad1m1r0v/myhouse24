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

    def handle_no_permission(self, request):
        if is_ajax(request):
            return JsonResponse(
                status=403,
                data={'success': False, 'message': self.permission_denied_message}
            )
        else:
            messages.error(request, self.permission_denied_message)
            logout(request)
            return redirect(reverse('authentication:adminlte:login'))

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission(request)
        return super().dispatch(request, *args, **kwargs)