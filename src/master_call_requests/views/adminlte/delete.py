from django.http import JsonResponse
from django.views import View

from .mixin import (
    HouseUserRequiredMixin,
    MasterCallRequestPermissionRequiredMixin
)
from ...models import MasterCallRequest


class AdminMasterCallRequestsDeleteView(
    HouseUserRequiredMixin,
    MasterCallRequestPermissionRequiredMixin,
    View
):
    def delete(self, request, *args, **kwargs):
        MasterCallRequest.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})