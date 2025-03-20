import time

from .mixin import PersonalAccountPermissionRequiredMixin
from django.views.generic import View

from django.http import HttpResponse
from django.views import View

from ...models import PersonalAccount
from ...services import AccountExcelService


class AdminAccountsExportView(
    PersonalAccountPermissionRequiredMixin,
    View):
    def post(self, request, *args, **kwargs):
        accounts = (PersonalAccount.objects
                    .with_balance()
                    .select_related('house', 'section', 'flat', 'flat__owner'))

        file = AccountExcelService.create_worksheet(accounts=accounts)

        response = HttpResponse(
            file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="accounts_{round(time.time() * 1000)}.xlsx"'
        return response
