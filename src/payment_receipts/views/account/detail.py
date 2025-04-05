from django.db.models import Prefetch
from django.views.generic import DetailView

from src.core.utils.permissions import OwnerRequiredMixin
from src.payment_receipts.models import Receipt, ReceiptService


class AccountReceiptDetailView(
    OwnerRequiredMixin,
    DetailView
):
    template_name = 'payment_receipts/account/detail.html'
    model = Receipt
    context_object_name = 'receipt'

    def get_queryset(self):
        services_qs = ReceiptService.objects.select_related('service', 'unit').with_total_price()

        return (super().get_queryset()
                .prefetch_related(Prefetch('services', queryset=services_qs))
                .with_total_price())
