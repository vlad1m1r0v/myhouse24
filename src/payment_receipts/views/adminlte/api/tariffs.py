from django.db.models import F
from django.http import JsonResponse
from django.views import View

from src.system_settings.models import Tariff
from ..mixin import ReceiptsPermissionRequiredMixin


class AdminReceiptsTariffsView(ReceiptsPermissionRequiredMixin,
                           View):
    def get(self, *args, **kwargs):
        term = self.request.GET.get('term', '')
        tariffs = Tariff.objects.filter(name__icontains=term).values('id', text=F('name'))
        return JsonResponse(data=list(tariffs), safe=False)