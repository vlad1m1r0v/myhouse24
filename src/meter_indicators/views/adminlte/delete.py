from django.http import JsonResponse
from django.views import View

from .mixin import (
    HouseUserRequiredMixin,
    MeterIndicatorPermissionRequiredMixin
)
from ...models import MeterIndicator


class AdminMeterIndicatorsDeleteView(
    HouseUserRequiredMixin,
    MeterIndicatorPermissionRequiredMixin,
    View
):
    def delete(self, request, *args, **kwargs):
        MeterIndicator.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})
