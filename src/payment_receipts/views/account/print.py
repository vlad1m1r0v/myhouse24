from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View

from src.core.utils.permissions import OwnerRequiredMixin
from src.payment_receipts.models import ReceiptTemplate
from src.payment_receipts.services import ReceiptExcelService, FileConverterService


class AccountReceiptPrintView(
    OwnerRequiredMixin,
    View
):
    def get(self, *args, **kwargs):
        receipt_id = self.kwargs['pk']

        template = ReceiptTemplate.objects.filter(is_selected=True).first()

        if not template:
            template = ReceiptTemplate.objects.first()

            if not template:
                messages.error(self.request, 'Не знайдено жодного шаблону')
                redirect(self.request.build_absolute_uri())

        output, filename = ReceiptExcelService.create_worksheet(receipt_id, template.id)
        pdf_file = FileConverterService.xlsx_to_pdf(output)

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{filename}.pdf"'

        return response
