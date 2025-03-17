from django.http import JsonResponse
from django.views import View

from .mixin import (
    HouseUserRequiredMixin,
    FlatOwnerPermissionRequiredMixin
)
from src.authentication.models import CustomUser


class AdminFlatOwnersDeleteView(
    HouseUserRequiredMixin,
    FlatOwnerPermissionRequiredMixin,
    View
):
    def delete(self, request, *args, **kwargs):
        CustomUser.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})