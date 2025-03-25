from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from src.payment_receipts.forms import AdminReceiptTemplateSelectForm
from src.payment_receipts.tasks import send_receipt
from src.payment_receipts.views.adminlte.mixin import (
    HouseUserRequiredMixin,
    ReceiptsPermissionRequiredMixin
)
from src.payment_receipts.models import Receipt, ReceiptTemplate
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

        default_template = ReceiptTemplate.objects.filter(is_selected=True).first()

        context['form'] = AdminReceiptTemplateSelectForm(
            initial={
                'template': default_template
            }
        )

        return context

    def post(self, *args, **kwargs):
        form = AdminReceiptTemplateSelectForm(self.request.POST)

        if form.is_valid():
            template_id = form.cleaned_data['template'].id
            receipt_id = kwargs.get('pk')

            if 'download' in self.request.POST:

                output, filename = ReceiptExcelService.create_worksheet(receipt_id, template_id)
                pdf_file = FileConverterService.xlsx_to_pdf(output)

                response = HttpResponse(pdf_file, content_type="application/pdf")
                response["Content-Disposition"] = f'inline; filename="{filename}.pdf"'

                return response

            elif 'send_email' in self.request.POST:
                send_receipt.delay(receipt_id, template_id)
                messages.success(self.request, 'Квитанція успішно відправлена')
                return redirect('adminlte:receipts:list')