from django.db.models import F
from django.http import JsonResponse
from django.views import View

from src.system_settings.models import TariffService
from ..mixin import ReceiptsPermissionRequiredMixin


class AdminReceiptsServicesView(
    ReceiptsPermissionRequiredMixin,
    View
):
    def get(self, *args, **kwargs):
        tariff_id = self.request.GET.get("tariff_id")

        if not tariff_id:
            services = TariffService.objects.none()
        else:
            services = (TariffService.objects.filter(tariff_id=tariff_id).
                        select_related('service', 'service__unit').
                        annotate(unit_id=F('service__unit_id')).
                        order_by('service_id').
                        values('service_id', 'unit_id', 'price'))

        return JsonResponse(data=list(services), safe=False)
