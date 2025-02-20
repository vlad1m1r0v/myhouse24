from django.db.models import Q, F, Value, CharField
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.views import View

from src.authentication.models import CustomUser
from ..mixin import (
    MasterCallRequestPermissionRequiredMixin,
)


class AdminMasterCallRequestsFlatOwnersView(MasterCallRequestPermissionRequiredMixin,
                                         View):
    def get(self, *args, **kwargs):
        term = self.request.GET.get('term')

        filters = Q()

        filters &= Q(is_staff=False)

        filters &= Q(status='active')

        if term:
            filters &= Q(text__icontains=term)

        flat_owners = (CustomUser.objects.
                       annotate(text=Concat('first_name', Value(' '), 'last_name')).
                       values('id', 'text', phone=F('phone_number')).
                       filter(filters))

        return JsonResponse(data=list(flat_owners), safe=False)
