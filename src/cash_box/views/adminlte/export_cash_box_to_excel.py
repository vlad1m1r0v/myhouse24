import time

from django.http import HttpResponse
from django.views import View

from src.flats.views.adminlte.mixin import HouseUserRequiredMixin
from .mixin import CashBoxPermissionRequiredMixin
from ...models import Transaction
from ...services import generate_cash_box_excel


class AdminCashBoxExportView(
    HouseUserRequiredMixin,
    CashBoxPermissionRequiredMixin,
    View):
    def post(self, *args, **kwargs):
        qs = (Transaction.objects
              .select_related('payment_item', 'owner', 'personal_account')
              .prefetch_related('personal_account__house__users'))

        if not self.request.user.is_superuser:
            qs = qs.filter(personal_account__house__users__in=[request.user.pk])

        file = generate_cash_box_excel(transactions=qs)

        response = HttpResponse(
            file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="cash_box_{round(time.time() * 1000)}.xlsx"'
        return response
