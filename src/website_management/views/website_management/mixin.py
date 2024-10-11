from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from src.core.utils import is_ajax


class WebsitePermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = 'authentication.website_management'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            if is_ajax(request):
                return JsonResponse(status=403,
                                    data={'success': False, 'message': 'У Вас немає доступу до управління сайтом'})
            else:
                messages.error(request, 'У Вас немає доступу до до управління сайтом')
                logout(request)
                return redirect(reverse('authentication_adminlte_login'))
        return super().dispatch(request, *args, **kwargs)