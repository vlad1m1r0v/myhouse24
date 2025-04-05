from datetime import datetime

from django.db.models import Prefetch, Sum, FloatField
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView

from src.cash_box.models import Transaction
from src.core.utils.permissions import OwnerRequiredMixin
from src.payment_receipts.models import ReceiptService, Receipt
from src.system_settings.models import PaymentCredential


class AccountReceiptPrintView(
    OwnerRequiredMixin,
    TemplateView
):
    template_name = 'payment_receipts/account/print.html'

    def get_context_data(self, **kwargs):
        receipt_id = self.kwargs.get('pk')

        context = super().get_context_data(**kwargs)

        services_qs = (ReceiptService.objects
                       .select_related('service', 'unit')
                       .with_total_price())

        receipt = (Receipt.objects
                   .prefetch_related(Prefetch('services', queryset=services_qs))
                   .with_total_price()
                   .select_related('personal_account', 'tariff', 'flat', 'flat__owner', 'house', 'section')
                   .get(pk=receipt_id))

        paid = Transaction.objects.filter(
            receipt_id=receipt_id,
            type='expense',
            is_complete=True
        ).aggregate(paid_sum=Coalesce(Sum('amount'), 0.0, output_field=FloatField()))['paid_sum']

        credential = PaymentCredential.objects.first()

        receipt_data = {
            'number': receipt.no,
            'date': receipt.date.strftime("%d.%m.%Y"),
            'today': datetime.today().strftime("%d.%m.%Y"),
            'period_from': f"{receipt.period_from.strftime('%d.%m.%Y')}",
            'period_to': f"{receipt.period_to.strftime('%d.%m.%Y')}",
            'company_name': credential.name,
            'company_information': credential.information,
            'full_name': f"{receipt.flat.owner}",
            'phone_number': receipt.flat.owner.phone_number,
            'email': receipt.flat.owner.email,
            'address': f"{receipt.house.address}, {receipt.section}, кв. № {receipt.flat.no}",
            'personal_account': receipt.personal_account.no,
            'sum': receipt.total_price,
            'paid': paid,
            'debt': receipt.total_price - paid,
            'services': [
                {
                    'index': index,
                    'name': service.service.name,
                    'value': service.value,
                    'unit': service.unit,
                    'price': service.price,
                    'total_price': service.total_price
                } for index, service in enumerate(receipt.services.all())
            ]
        }

        context['receipt'] = receipt_data

        return context
