from django.db.models import F
from django.http import JsonResponse
from django.views import View

from src.houses.models import HouseFloor
from ..mixin import FlatPermissionRequiredMixin

'''
Example of View for processing AJAX calls with pagination support
'''


class AdminFlatFloorsView(FlatPermissionRequiredMixin,
                          View):
    def get(self, *args, **kwargs):
        house_id = self.request.GET.get('house_id')

        page = int(self.request.GET.get('page', 1))
        term = self.request.GET.get('term', '')

        if not house_id:
            queryset = HouseFloor.objects.none()
        else:
            queryset = HouseFloor.objects.filter(house__id=house_id, name__icontains=term)

        data = {
            'results': list(queryset[10 * (page - 1): 10 * page].values('id', text=F('name'))),
            'pagination': {
                'more': queryset.count() > 10 * page
            }
        }

        return JsonResponse(data=data, safe=False)
