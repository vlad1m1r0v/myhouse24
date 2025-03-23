from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from src.payment_receipts.models import ReceiptTemplate
from src.payment_receipts.views.adminlte.mixin import ReceiptsPermissionRequiredMixin


class AdminReceiptTemplatesDeleteView(
    SuccessMessageMixin,
    ReceiptsPermissionRequiredMixin,
    DeleteView
):
    model = ReceiptTemplate
    success_message = 'Шаблон для квитанції успішно видалено'
    success_url = reverse_lazy('adminlte:receipts:templates:index')