from django.http import JsonResponse
from django.views import View
from django.db.models import Q, F

from src.houses.models import House
from ..mixin import PersonalAccountPermissionRequiredMixin


class AdminPersonalAccountHousesView(PersonalAccountPermissionRequiredMixin,
                                     View):
    def get(self, *args, **kwargs):
        term = self.request.GET.get('term', '')
        user = self.request.user

        filters = Q()

        filters &= Q(name__icontains=term)

        if not user.is_superuser:
            filters &= Q(users__user=user)

        houses = House.objects.filter(filters).values("id", text=F("name"))

        return JsonResponse(data=list(houses), safe=False)
