from django.db.models import Value
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.views import View

from src.authentication.models import CustomUser
from ..mixin import CashBoxPermissionRequiredMixin


class AdminCashBoxOwnersView(CashBoxPermissionRequiredMixin,
                          View):
    def get(self, *args, **kwargs):
        term = self.request.GET.get('term', '')

        owners = (CustomUser.objects
                  .annotate(text=Concat('first_name', Value(' '), 'last_name'))
                  .filter(is_staff=False, status='active', text__icontains=term).values('text', 'id'))

        return JsonResponse(data=list(owners), safe=False)