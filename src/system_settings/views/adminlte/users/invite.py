from django.http import JsonResponse
from django.views import View

from src.system_settings.tasks import send_invitation_email
from src.authentication.models import CustomUser

from .mixin import UserPermissionRequiredMixin


class AdminUserInviteView(
    UserPermissionRequiredMixin,
    View
):
    def post(self, request, *args, **kwargs):
        email = CustomUser.objects.get(pk=kwargs['pk']).email
        send_invitation_email.delay(email)
        return JsonResponse(status=200, data={'success': True})
