from django.db import models

from src.authentication.models import CustomUser
from src.personal_accounts.models import PersonalAccount
from src.system_settings.models import PaymentItem


class TypeChoices(models.TextChoices):
    INCOME = 'income', 'надходження'
    EXPENSE = 'expense', 'витрата'


class Transaction(models.Model):
    no = models.CharField(max_length=20)
    date = models.DateField()
    type = models.CharField(choices=TypeChoices.choices, default=TypeChoices.EXPENSE)
    owner = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE,
                              related_name='owner_transactions')
    personal_account = models.ForeignKey(PersonalAccount, null=True, blank=True, on_delete=models.CASCADE,
                                         related_name='account_transactions')
    payment_item = models.ForeignKey(PaymentItem, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=1)
    is_complete = models.BooleanField(default=False)
    manager = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='manager_transactions')
    comment = models.TextField()
