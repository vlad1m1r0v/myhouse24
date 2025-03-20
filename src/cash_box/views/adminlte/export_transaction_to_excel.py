from django.http import HttpResponse
from django.views import View

from .mixin import (
    CashBoxPermissionRequiredMixin,
    HouseUserRequiredMixin
)
from ...models import Transaction
from ...services import TransactionExcelService


class AdminTransactionExportView(
    HouseUserRequiredMixin,
    CashBoxPermissionRequiredMixin,
    View):
    def post(self,  request, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = Transaction.objects.get(pk=pk)
        file = TransactionExcelService.create_worksheet(transaction=obj)

        response = HttpResponse(
            file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="transaction_{obj.no}.xlsx"'
        return response
