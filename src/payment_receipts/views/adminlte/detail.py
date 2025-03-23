from django.db.models import Prefetch
from django.views.generic import DetailView

from .mixin import (
    HouseUserRequiredMixin,
    ReceiptsPermissionRequiredMixin
)
from ...models import Receipt, ReceiptService


class AdminReceiptDetailView(
    ReceiptsPermissionRequiredMixin,
    HouseUserRequiredMixin,
    DetailView
):
    template_name = 'payment_receipts/adminlte/detail.html'
    model = Receipt
    context_object_name = 'receipt'

    def get_queryset(self, **kwargs):
        services_qs = ReceiptService.objects.select_related('service', 'unit').with_total_price()

        return (super().get_queryset()
                .prefetch_related(Prefetch('services', queryset=services_qs))
                .with_total_price()
                .select_related('personal_account', 'tariff', 'flat', 'flat__owner', 'house', 'section'))
