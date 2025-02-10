from django.db.models import Value, F
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.views import View

from src.flats.models import Flat
from ..mixin import PersonalAccountPermissionRequiredMixin


class AdminPersonalAccountOwnerView(PersonalAccountPermissionRequiredMixin,
                                    View):
    def get(self, request, *args, **kwargs):
        flat_id = self.request.GET.get('flat_id')

        owner = (Flat.objects.select_related('owner').annotate(
            name=Concat('owner__first_name', Value(' '), 'owner__last_name'),
            phone=F('owner__phone_number')
        ).values('name', 'phone', identifier=F('owner__pk')).get(pk=flat_id))

        return JsonResponse(data=owner, safe=False)
