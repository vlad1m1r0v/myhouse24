from datetime import timedelta
from django.http import JsonResponse
from django.utils.formats import date_format
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.views import View

from src.dashboard.utils import get_last_12_months
from ..mixin import StatisticsPermissionRequiredMixin
from src.cash_box.models import Transaction, TypeChoices


class AdminDashboardCashBoxChartView(
    StatisticsPermissionRequiredMixin,
    View
):
    def get(self, *args, **kwargs):
        last_12_months = get_last_12_months()

        user = self.request.user
        is_superuser = user.is_superuser

        expense_query = Transaction.objects.filter(
            type=TypeChoices.EXPENSE,
            is_complete=True,
            personal_account__isnull=True,
            receipt__isnull=True,
            date__gte=last_12_months[0],
            date__lte=last_12_months[-1] + timedelta(days=31)
        ).annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total_expense=Sum('amount')
        ).order_by('month')

        income_query = Transaction.objects.filter(
            type=TypeChoices.INCOME,
            is_complete=True,
            personal_account__isnull=True,
            receipt__isnull=True,
            date__gte=last_12_months[0],
            date__lte=last_12_months[-1] + timedelta(days=31)
        ).annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total_income=Sum('amount')
        ).order_by('month')

        if not is_superuser:
            income_query = income_query.filter(personal_account__house__users__user=user)
            expense_query = expense_query.filter(personal_account__house__users__user=user)

        expense_dict = {e["month"]: e["total_expense"] for e in expense_query}
        income_dict = {i["month"]: i["total_income"] for i in income_query}

        result = []
        for month in last_12_months:
            month_name = date_format(month, "F", use_l10n=True)
            result.append({
                "month": month_name,
                "expense": expense_dict.get(month, 0) or 0,
                "income": income_dict.get(month, 0) or 0,
            })

        return JsonResponse(result, safe=False)
