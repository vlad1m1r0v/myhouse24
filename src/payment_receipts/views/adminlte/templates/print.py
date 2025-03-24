from django.http import HttpResponse
from django.views.generic import TemplateView

from src.payment_receipts.forms import AdminReceiptTemplateSelectForm
from src.payment_receipts.views.adminlte.mixin import (
    HouseUserRequiredMixin,
    ReceiptsPermissionRequiredMixin
)
from src.payment_receipts.models import Receipt
from src.payment_receipts.services import (
    ReceiptExcelService,
    FileConverterService
)


class AdminReceiptPrintView(
    ReceiptsPermissionRequiredMixin,
    HouseUserRequiredMixin,
    TemplateView,
):
    template_name = 'payment_receipts/adminlte/template_print.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['receipt'] = Receipt.objects.get(pk=self.kwargs['pk'])
        context['form'] = AdminReceiptTemplateSelectForm()

        return context

    def post(self, *args, **kwargs):
        form = AdminReceiptTemplateSelectForm(self.request.POST)

        if form.is_valid():
            template_id = form.cleaned_data['template'].id
            receipt_id = kwargs.get('pk')

            output, filename = ReceiptExcelService.create_worksheet(receipt_id, template_id)
            pdf_file = FileConverterService.xlsx_to_pdf(output)

            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = f'inline; filename="{filename}.pdf"'

            return response
