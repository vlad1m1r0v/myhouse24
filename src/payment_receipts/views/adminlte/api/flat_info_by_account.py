from django.http import JsonResponse
from django.views import View

from src.personal_accounts.models import PersonalAccount
from ..mixin import ReceiptsPermissionRequiredMixin


class AdminReceiptsFlatInfoByAccountView(ReceiptsPermissionRequiredMixin, View):
    def get(self, *args, **kwargs):
        account_no = self.request.GET.get('account_no')

        personal_account = PersonalAccount.objects.select_related(
            'flat__house', 'flat__section', 'flat__owner', 'flat__tariff'
        ).get(no=account_no)

        if not personal_account.flat:
            return JsonResponse({'error': 'Цей рахунок не прив’язаний до квартири'}, status=400)

        flat = personal_account.flat

        flat_data = {
            'house_id': flat.house.id,
            'house_name': flat.house.name,
            'section_id': flat.section.id,
            'section_name': flat.section.name,
            'flat_id': flat.id,
            'flat_name': f"{flat.no}, {flat.house.name}",
            'account_no': personal_account.no,
            'owner_id': flat.owner.id if flat.owner else None,
            'owner_name': f"{flat.owner.last_name} {flat.owner.first_name} {flat.owner.middle_name}" if flat.owner else "Немає власника",
            'owner_phone': flat.owner.phone_number,
            'tariff_id': flat.tariff.id if flat.tariff else None,
            'tariff_name': flat.tariff.name if flat.tariff else "Не вказано",
        }

        return JsonResponse(data=flat_data, safe=False)
