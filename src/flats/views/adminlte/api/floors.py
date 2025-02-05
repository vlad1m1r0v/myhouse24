from django.db.models import F
from django.http import JsonResponse
from django.views import View

from src.houses.models import HouseFloor
from ..mixin import FlatPermissionRequiredMixin


class AdminFlatFloorsView(FlatPermissionRequiredMixin,
                          View):
    def get(self, *args, **kwargs):
        house_id = self.request.GET.get('house_id')
        term = self.request.GET.get('term', '')

        if not house_id:
            floors = HouseFloor.objects.none().values('id', text=F('name'))
        else:
            floors = HouseFloor.objects.filter(house__id=house_id, name__icontains=term).values('id', text=F('name'))

        return JsonResponse(data=list(floors), safe=False)
