from django.views.generic import TemplateView

from src.core.utils.permissions import OwnerRequiredMixin
from src.payment_receipts.models import Receipt
from src.system_settings.models import PaymentCredential


class AccountReceiptPayView(
    OwnerRequiredMixin,
    TemplateView
):
    template_name = 'payment_receipts/account/pay.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        receipt_id = self.kwargs.get('pk')
        receipt = (Receipt.objects.
                   select_related('personal_account').
                   with_total_price().get(pk=receipt_id))
        context['receipt'] = receipt

        context['payment_credential'] = PaymentCredential.objects.first()

        return context
