from django.db.models import F
from django.http import JsonResponse
from django.views import View

from src.system_settings.models import Service
from ..mixin import MeterIndicatorPermissionRequiredMixin


class AdminMeterIndicatorsServicesView(MeterIndicatorPermissionRequiredMixin,
                                       View):
    def get(self, *args, **kwargs):
        term = self.request.GET.get('term', '')

        services = Service.objects.filter(name__icontains=term).values('id', text=F('name'))

        return JsonResponse(data=list(services), safe=False)
