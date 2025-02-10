from django.db.models import F
from django.http import JsonResponse
from django.views import View

from src.houses.models import HouseSection
from ..mixin import PersonalAccountPermissionRequiredMixin


class AdminPersonalAccountSectionsView(PersonalAccountPermissionRequiredMixin,
                            View):
    def get(self, *args, **kwargs):
        house_id = self.request.GET.get('house_id')
        term = self.request.GET.get('term', '')

        if not house_id:
            sections = HouseSection.objects.none().values('id', text=F('name'))
        else:
            sections = HouseSection.objects.filter(house__id=house_id, name__icontains=term).values('id', text=F('name'))

        return JsonResponse(data=list(sections), safe=False)