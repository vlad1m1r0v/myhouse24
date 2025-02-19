from django.db.models import Value, F, Q
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.views import View

from src.authentication.models import CustomUser
from ..mixin import MasterCallRequestPermissionRequiredMixin


class AdminMasterCallRequestMastersView(
    MasterCallRequestPermissionRequiredMixin,
    View):
    def get(self, *args, **kwargs):
        group_id = self.request.GET.get('group_id')
        term = self.request.GET.get('term')

        filters = Q()

        if term:
            filters &= Q(text__icontains=term)

        if group_id:
            filters &= Q(groups__id=group_id)
        else:
            filters &= Q(groups__name__in=['Сантехнік', 'Електрик'])

        masters = CustomUser.objects.annotate(
            text=Concat(
                F('first_name'),
                Value(' '),
                F('last_name'),
            )
        ).filter(filters).values('id', 'text')

        return JsonResponse(data=list(masters), safe=False)
