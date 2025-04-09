from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.db.models.aggregates import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from src.cash_box.models import Transaction, TypeChoices
from src.core.utils.permissions import OwnerRequiredMixin
from src.payment_receipts.models import Receipt, ReceiptService
from src.personal_accounts.models import PersonalAccount
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

    def post(self, *args, **kwargs):
        receipt_id = kwargs.get('pk')

        receipt = Receipt.objects.with_total_price().get(pk=receipt_id)
        personal_account = PersonalAccount.objects.with_balance().get(pk=receipt.personal_account_id)

        total = receipt.total_price
        balance = personal_account.balance
        paid = Transaction.objects.filter(
            receipt_id=receipt_id,
            is_complete=True,
            type=TypeChoices.EXPENSE
        ).aggregate(
            total_amount=Coalesce(Sum('amount'), Decimal(0))
        )['total_amount']
        left = total - float(paid)

        if balance == 0:
            messages.error(self.request, "На рахунку немає коштів")
            return redirect(reverse('account:receipts:list'))

        if balance < left:
            transaction = Transaction.objects.create(
                receipt=receipt,
                no=int(datetime.now().timestamp() * 1000),
                date=datetime.now().date(),
                type=TypeChoices.EXPENSE,
                owner=self.request.user,
                personal_account=personal_account,
                amount=balance,
                is_complete=True
            )

            receipt.status = 'partially_paid'

            transaction.save()
            receipt.save()

            messages.success(self.request, "Квитанційна частково оплачена")
            return redirect(reverse('account:receipts:list'))
        else:
            transaction = Transaction.objects.create(
                receipt=receipt,
                no=int(datetime.now().timestamp() * 1000),
                date=datetime.now().date(),
                type=TypeChoices.EXPENSE,
                owner=self.request.user,
                personal_account=personal_account,
                amount=left,
                is_complete=True
            )

            receipt.status = 'paid'

            receipt_services = (ReceiptService.objects.
                                select_related('meter_indicator').
                                filter(receipt_id=receipt_id))

            for service in receipt_services:
                service.meter_indicator.status = 'accounted_paid'
                service.meter_indicator.save()

            transaction.save()
            receipt.save()

            messages.success(self.request, "Квитанційна повністю оплачена")
            return redirect(reverse('account:receipts:list'))
