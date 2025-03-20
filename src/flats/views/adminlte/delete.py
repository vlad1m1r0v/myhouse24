from django.http import JsonResponse
from django.views import View

from .mixin import (
    FlatPermissionRequiredMixin,
    HouseUserRequiredMixin
)
from ...models import Flat


class AdminFlatsDeleteView(
    FlatPermissionRequiredMixin,
    HouseUserRequiredMixin,
    View):
    def delete(self, request, *args, **kwargs):
        Flat.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})