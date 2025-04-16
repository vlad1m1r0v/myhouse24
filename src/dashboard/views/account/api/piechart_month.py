from datetime import date, timedelta

from django.http import JsonResponse
from django.views import View

from src.cash_box.models import Transaction
from src.core.utils.permissions import OwnerRequiredMixin


class AccountDashboardPiechartMonthView(
    OwnerRequiredMixin,
    View
):
    def get(self, *args, **kwargs):
        flat_id = self.request.GET.get('flat_id')

        today = date.today()
        start_date = date.today() - timedelta(days=30)

        transactions = Transaction.objects.filter(
            type='expense',
            is_complete=True,
            receipt__flat_id=flat_id,
            date__gte=start_date
        ).select_related('receipt__flat')

        service_totals = {}

        for transaction in transactions:
            receipt = transaction.receipt

            if not receipt:
                continue

            services = receipt.services.all()
            full_receipt_total = sum(float(s.price) * s.value for s in services)

            if full_receipt_total == 0:
                continue

            transaction_ratio = float(transaction.amount) / full_receipt_total

            for s in services:
                service_name = s.service.name
                service_total = float(s.price) * s.value * transaction_ratio

                if service_name not in service_totals:
                    service_totals[service_name] = 0

                service_totals[service_name] += round(service_total, 2)

        return JsonResponse(service_totals)
