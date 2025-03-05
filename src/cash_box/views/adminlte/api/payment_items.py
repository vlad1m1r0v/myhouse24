from django.db.models import Q, F
from django.http import JsonResponse
from django.views import View

from src.system_settings.models import PaymentItem
from ..mixin import CashBoxPermissionRequiredMixin


class AdminCashBoxPaymentItemsView(CashBoxPermissionRequiredMixin,
                               View):
    def get(self, *args, **kwargs):
        term = self.request.GET.get('term', '')
        payment_item_type = self.request.GET.get('type')

        filters = Q()

        if term:
            filters &= Q(name__icontains=term)

        if payment_item_type:
            filters &= Q(type=payment_item_type)

        qs = PaymentItem.objects.filter(filters)

        payment_items = qs.annotate(text=F('name')).values('id', 'text')

        return JsonResponse(data=list(payment_items), safe=False)
