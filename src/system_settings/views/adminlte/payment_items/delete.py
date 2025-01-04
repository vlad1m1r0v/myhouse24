from django.http import JsonResponse
from django.views import View

from src.system_settings.models import PaymentItem
from .mixin import PaymentItemPermissionRequiredMixin


class AdminPaymentItemsDeleteView(PaymentItemPermissionRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        PaymentItem.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})
