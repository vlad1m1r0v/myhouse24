from django.db.models import Q, F, Value, CharField
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.views import View

from src.flats.models import Flat
from ..mixin import MasterCallRequestPermissionRequiredMixin


class AdminMasterCallRequestsFlatsView(MasterCallRequestPermissionRequiredMixin,
                                       View):
    def get(self, *args, **kwargs):
        user = self.request.user

        owner_id = self.request.GET.get('owner_id')
        term = self.request.GET.get('term')

        if not owner_id:
            flats = Flat.objects.none()

        else:
            filters = Q()

            filters &= Q(owner_id=owner_id)

            if not user.is_superuser:
                filters &= Q(house__users__user=user)

            if term:
                filters &= Q(no__icontains=term)

            flats = (Flat.objects.
                     select_related('house', 'section', 'floor').
                     filter(filters).values('id',
                                            'house_id',
                                            house_name=F('house__name'),
                                            section_name=F('section__name'),
                                            floor_name=F('floor__name'),
                                            text=Concat(
                                                Value('Квартира № '),
                                                F('no'),
                                                output_field=CharField())))

        return JsonResponse(data=list(flats), safe=False)
