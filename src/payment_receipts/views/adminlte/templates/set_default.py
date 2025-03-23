from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import View

from src.payment_receipts.models import ReceiptTemplate
from src.payment_receipts.views.adminlte.mixin import ReceiptsPermissionRequiredMixin


class AdminReceiptsTemplateSetDefaultView(
    ReceiptsPermissionRequiredMixin,
    View
):

    def post(self, *args, **kwargs):
        template_id = self.kwargs.get('pk')

        ReceiptTemplate.objects.all().update(is_selected=False)
        ReceiptTemplate.objects.filter(pk=template_id).update(is_selected=True)

        messages.success(self.request, 'Новий шаблон за замовчуванням успішно вибрано')
        return redirect('adminlte:receipts:templates:index')
