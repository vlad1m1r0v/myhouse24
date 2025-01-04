from django.http import JsonResponse
from django.views import View

from src.authentication.models import CustomUser
from .mixin import UserPermissionRequiredMixin


class AdminUserDeleteView(
    UserPermissionRequiredMixin,
    View
):
    def delete(self, request, *args, **kwargs):
        CustomUser.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})
