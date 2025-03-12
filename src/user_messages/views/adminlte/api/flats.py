from django.db.models import Q, F, Value, CharField
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.views import View

from src.flats.models import Flat
from ..mixin import MessagePermissionRequiredMixin


class AdminMessagesFlatsView(MessagePermissionRequiredMixin,
                             View):
    def get(self, *args, **kwargs):
        section_id = self.request.GET.get('section_id')
        floor_id = self.request.GET.get('floor_id')
        term = self.request.GET.get('term')

        if not section_id or not floor_id:
            flats = Flat.objects.none()

        else:
            filters = Q()

            filters &= Q(section_id=section_id)
            filters &= Q(floor_id=floor_id)

            if term:
                filters &= Q(no__icontains=term)

            flats = Flat.objects.filter(filters).values('id',
                                                        text=Concat(
                                                            Value('Квартира № '),
                                                            F('no'),
                                                            output_field=CharField()))

        return JsonResponse(data=list(flats), safe=False)
