from django.db.models import Sum

from src.cash_box.models import Transaction, TypeChoices
from src.payment_receipts.models import Receipt


class AdminBalanceMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ----------CASH BOX BALANCE----------
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

        # ----------PERSONAL ACCOUNT BALANCE----------
        income_transactions = Transaction.objects.filter(
            type=TypeChoices.INCOME,
            personal_account__isnull=False,
            is_complete=True
        )

        if not self.request.user.is_superuser:
            income_transactions = income_transactions.filter(
                personal_account__house__users__user=self.request.user
            )

        account_income = income_transactions.aggregate(Sum('amount'))['amount__sum'] or 0

        expense_transactions = Transaction.objects.filter(
            type=TypeChoices.EXPENSE,
            personal_account__isnull=False,
            is_complete=True
        )

        if not self.request.user.is_superuser:
            expense_transactions = expense_transactions.filter(
                personal_account__house__users__user=self.request.user
            )

        account_expense = expense_transactions.aggregate(Sum('amount'))['amount__sum'] or 0

        context['account_balance'] = account_income - account_expense

        # ----------RECEIPT DEBT----------
        receipts = Receipt.objects.with_total_price().filter(personal_account__isnull=False)

        if not self.request.user.is_superuser:
            receipts = income_transactions.filter(house__users__user=self.request.user)

        total_debt = receipts.aggregate(Sum('total_price'))['total_price__sum'] or 0

        debt_paid_transactions = Transaction.objects.filter(
            type=TypeChoices.EXPENSE,
            personal_account__isnull=False,
            receipt__isnull=False,
            is_complete=True
        )

        if not self.request.user.is_superuser:
            debt_paid_transactions = debt_paid_transactions.filter(
                personal_account__house__users__user=self.request.user
            )

        debt_paid = debt_paid_transactions.aggregate(Sum('amount'))['amount__sum'] or 0

        context['receipt_debt'] = total_debt - debt_paid

        return context
