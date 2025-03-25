from datetime import timedelta
from django.http import JsonResponse
from django.utils.formats import date_format
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.views import View

from src.dashboard.utils import get_last_12_months
from ..mixin import StatisticsPermissionRequiredMixin
from src.payment_receipts.models import Receipt
from src.cash_box.models import Transaction, TypeChoices


class AdminDashboardReceiptChartView(
    StatisticsPermissionRequiredMixin,
    View
):
    def get(self, *args, **kwargs):
        last_12_months = get_last_12_months()

        user = self.request.user
        is_superuser = user.is_superuser

        receipts_query = Receipt.objects.with_total_price().filter(
            date__gte=last_12_months[0],
            date__lte=last_12_months[-1] + timedelta(days=31)
        ).annotate(
            month=TruncMonth('date')
        ).values('month', 'total_price').order_by('month')

        transactions_query = Transaction.objects.filter(
            type=TypeChoices.EXPENSE,
            is_complete=True,
            personal_account__isnull=False,
            receipt__isnull=False,
            date__gte=last_12_months[0],
            date__lte=last_12_months[-1] + timedelta(days=31)
        ).annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total_paid=Sum('amount')
        ).order_by('month')

        if not is_superuser:
            receipts_query = receipts_query.filter(house__users__user=user)
            transactions_query = transactions_query.filter(personal_account__house__users__user=user)

        receipts_dict = {r["month"]: r["total_price"] for r in receipts_query}
        transactions_dict = {t["month"]: t["total_paid"] for t in transactions_query}

        result = []
        for month in last_12_months:
            month_name = date_format(month, "F", use_l10n=True)
            result.append({
                "month": month_name,
                "debt": receipts_dict.get(month, 0) or 0,
                "paid": transactions_dict.get(month, 0) or 0,
            })

        return JsonResponse(result, safe=False)
