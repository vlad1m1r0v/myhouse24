from django.http import JsonResponse
from django.views import View

from .mixin import (
    ReceiptsPermissionRequiredMixin,
    HouseUserRequiredMixin
)
from ...models import Receipt


class AdminReceiptsDeleteView(
    ReceiptsPermissionRequiredMixin,
    HouseUserRequiredMixin,
    View):
    def delete(self, request, *args, **kwargs):
        Receipt.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})