from django.http import JsonResponse
from django.views import View

from src.flats.models import Flat
from ..mixin import ReceiptsPermissionRequiredMixin


class AdminReceiptsFlatInfoView(ReceiptsPermissionRequiredMixin, View):
    def get(self, *args, **kwargs):
        flat_id = self.request.GET.get('flat_id')

        flat = Flat.objects.select_related('owner', 'tariff', 'personal_account').get(pk=flat_id)

        flat_data = {
            'account_no': flat.personal_account.no if hasattr(flat, 'personal_account') else None,
            'owner_id': flat.owner.id if flat.owner else None,
            'owner_name': f"{flat.owner.last_name} {flat.owner.first_name} {flat.owner.middle_name}" if hasattr(flat, 'owner') else "Немає власника",
            'owner_phone': flat.owner.phone_number,
            'tariff_id': flat.tariff.id if hasattr(flat, 'tariff') else None,
            'tariff_name': flat.tariff.name if hasattr(flat, 'tariff') else "Не вказано",
        }

        return JsonResponse(data=flat_data, safe=False)
