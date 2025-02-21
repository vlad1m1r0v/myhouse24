from django.http import JsonResponse
from django.urls import reverse
from django.views import View

from src.system_settings.tasks import send_invitation_email
from src.authentication.models import CustomUser

from .mixin import UserPermissionRequiredMixin


class AdminUserInviteView(
    UserPermissionRequiredMixin,
    View
):
    def post(self, *args, **kwargs):
        email = CustomUser.objects.get(pk=kwargs['pk']).email
        login_path = reverse('authentication:adminlte:login')
        login_url = self.request.build_absolute_uri(login_path)

        send_invitation_email.delay(email, login_url)
        return JsonResponse(status=200, data={'success': True})
