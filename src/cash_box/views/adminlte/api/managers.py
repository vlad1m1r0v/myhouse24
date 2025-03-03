from django.contrib.auth.models import Group
from django.db.models import Value, Subquery, OuterRef, Q
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.views import View

from src.authentication.models import CustomUser
from ..mixin import CashBoxPermissionRequiredMixin


class AdminCashBoxManagersView(CashBoxPermissionRequiredMixin,
                               View):
    def get(self, *args, **kwargs):
        term = self.request.GET.get('term', '')

        role_subquery = Subquery(Group.objects.filter(user=OuterRef('pk')).order_by('id')[:1].values('name'))

        filters = Q()

        filters &= Q(role='Бухгалтер') | Q(role='Керуючий') | Q(role='Директор')

        if term:
            filters &= Q(text__icontains=term)

        managers = (CustomUser.objects
                    .annotate(role=role_subquery)
                    .annotate(text=Concat('first_name', Value(' '), 'last_name', Value(' - '), 'role'))
                    .filter(filters)
                    .values('text', 'id'))

        return JsonResponse(data=list(managers), safe=False)
