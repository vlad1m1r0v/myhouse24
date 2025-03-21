from django.db.models import Sum

from src.cash_box.models import Transaction, TypeChoices
from src.payment_receipts.models import Receipt


class AdminBalanceMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cash_income = Transaction.objects.filter(
            type=TypeChoices.INCOME,
            personal_account__isnull=True,
            is_complete=True
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        cash_expense = Transaction.objects.filter(
            type=TypeChoices.EXPENSE,
            personal_account__isnull=True,
            is_complete=True
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        context['cash_balance'] = cash_income - cash_expense

        account_income = Transaction.objects.filter(
            type=TypeChoices.INCOME,
            personal_account__isnull=False,
            is_complete=True
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        account_expense = Transaction.objects.filter(
            type=TypeChoices.EXPENSE,
            personal_account__isnull=False,
            is_complete=True
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        context['account_balance'] = account_income - account_expense

        total_debt = (Receipt.objects
                      .with_total_price()
                      .filter(personal_account__isnull=False)
                      .aggregate(Sum('total_price'))['total_price__sum'] or 0)

        debt_paid = Transaction.objects.filter(
            type=TypeChoices.EXPENSE,
            personal_account__isnull=False,
            receipt__isnull=False,
            is_complete=True
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        context['receipt_debt'] = total_debt - debt_paid

        return context
