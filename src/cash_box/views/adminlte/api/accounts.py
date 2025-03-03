from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.views import View

from src.personal_accounts.models import PersonalAccount
from ..mixin import CashBoxPermissionRequiredMixin


class AdminCashBoxAccountsView(CashBoxPermissionRequiredMixin,
                               View):
    def get(self, *args, **kwargs):
        term = self.request.GET.get('term', '')
        owner_id = self.request.GET.get('owner_id')

        filters = Q()

        if not owner_id:
            qs = PersonalAccount.objects.none()
        else:
            filters &= Q(no__icontains=term)
            filters &= Q(status='active')
            filters &= Q(flat__owner_id=owner_id)

            qs = PersonalAccount.objects.filter(filters)

        accounts = (qs.
                    annotate(text=Concat(Value('Особовий рахунок № '), F('no'))).
                    values('id', 'text'))

        return JsonResponse(data=list(accounts), safe=False)
