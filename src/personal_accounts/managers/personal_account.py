from django.db import models
from django.db.models import Sum, Case, When, Value, Exists, OuterRef, DecimalField, F
from django.db.models.functions import Coalesce

from src.cash_box.models import TypeChoices
from src.payment_receipts.models import Receipt


class PersonalAccountQuerySet(models.QuerySet):
    def with_debt(self):
        return self.annotate(
            has_debt=Exists(
                Receipt.objects.filter(
                    personal_account_id=OuterRef("pk"),
                    status__in=["unpaid", "partially_paid"]
                )
            )
        )

    def with_balance(self):
        return self.annotate(
            income=Coalesce(
                Sum(
                    Case(
                        When(
                            account_transactions__type=TypeChoices.INCOME,
                            account_transactions__is_complete=True,
                            then=F("account_transactions__amount")
                        ),
                        default=Value(0.0),
                        output_field=DecimalField()
                    )
                ),
                Value(0.0),
                output_field=DecimalField()
            ),
            expense=Coalesce(
                Sum(
                    Case(
                        When(
                            account_transactions__type=TypeChoices.EXPENSE,
                            account_transactions__is_complete=True,
                            account_transactions__receipt__isnull=False,
                            then=F("account_transactions__amount")
                        ),
                        default=Value(0.0),
                        output_field=DecimalField()
                    )
                ),
                Value(0.0),
                output_field=DecimalField()
            ),
            balance=F("income") - F("expense")
        )

class PersonalAccountManager(models.Manager):
    def get_queryset(self):
        return PersonalAccountQuerySet(self.model, using=self._db)

    def with_debt(self):
        return self.get_queryset().with_debt()

    def with_balance(self):
        return self.get_queryset().with_balance()