from datetime import date

from dateutil.relativedelta import relativedelta
from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from src.cash_box.models import Transaction
from src.core.utils.permissions import OwnerRequiredMixin


class AccountMonthlyExpensesView(OwnerRequiredMixin, View):
    def get(self, *args, **kwargs):
        flat_id = self.request.GET.get('flat_id')

        today = date.today()
        start_date = today - relativedelta(months=11)
        start_date = start_date.replace(day=1)

        transactions = Transaction.objects.filter(
            type='expense',
            is_complete=True,
            receipt__isnull=False,
            receipt__flat_id=flat_id,
            date__gte=start_date
        ).select_related('receipt')

        monthly_totals = {}

        for tx in transactions:
            receipt = tx.receipt
            services = receipt.services.all()
            full_total = sum(float(s.price) * s.value for s in services)
            if full_total == 0:
                continue

            ratio = float(tx.amount) / full_total
            total_tx_value = sum(float(s.price) * s.value * ratio for s in services)

            key = (tx.date.year, tx.date.month)
            monthly_totals[key] = monthly_totals.get(key, 0) + round(total_tx_value, 2)

        result = []
        for i in range(12):
            dt = start_date + relativedelta(months=i)
            key = (dt.year, dt.month)
            month_label = dt.strftime('%B').capitalize()
            result.append({
                'month': _(month_label),
                'amount': round(monthly_totals.get(key, 0), 2)
            })

        return JsonResponse(result, safe=False)