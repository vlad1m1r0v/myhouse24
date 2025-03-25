from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage

from src.payment_receipts.models import Receipt
from src.payment_receipts.services import ReceiptExcelService, FileConverterService


@shared_task
def send_receipt(receipt_id, template_id):
    output, filename = ReceiptExcelService.create_worksheet(receipt_id, template_id)
    pdf_file = FileConverterService.xlsx_to_pdf(output)

    receipt = Receipt.objects.select_related('flat', 'flat__owner').get(pk=receipt_id)
    email = receipt.flat.owner.email

    subject = 'Квитанція на оплату'

    email_message = EmailMessage(
        subject=subject,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )

    email_message.attach(f"{filename}.pdf", pdf_file.read(), "application/pdf")

    email_message.send()