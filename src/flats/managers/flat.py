from django.db import models
from django.db.models import Exists, OuterRef, Value, Sum, Case, When, F
from django.db.models.functions import Coalesce

from src.cash_box.models import TypeChoices
from src.payment_receipts.models import Receipt


class FlatQuerySet(models.QuerySet):
    def with_debt(self):
        return self.annotate(
            has_debt=Exists(
                Receipt.objects.filter(
                    flat_id=OuterRef("pk"),
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
                            personal_account__account_transactions__type=TypeChoices.INCOME,
                            personal_account__account_transactions__is_complete=True,
                            then=F("personal_account__account_transactions__amount")
                        ),
                        default=Value(0.0),
                        output_field=models.DecimalField()
                    )
                ),
                Value(0.0),
                output_field=models.DecimalField()
            ),
            expense=Coalesce(
                Sum(
                    Case(
                        When(
                            personal_account__account_transactions__type=TypeChoices.EXPENSE,
                            personal_account__account_transactions__is_complete=True,
                            personal_account__account_transactions__receipt__isnull=False,
                            then=F("personal_account__account_transactions__amount")
                        ),
                        default=Value(0.0),
                        output_field=models.DecimalField()
                    )
                ),
                Value(0.0),
                output_field=models.DecimalField()
            )
        ).annotate(balance=F("income") - F("expense"))

    def with_related(self):
        return self.select_related("house", "section", "floor", "tariff", "personal_account")

class FlatManager(models.Manager):
    def get_queryset(self):
        return FlatQuerySet(self.model, using=self._db)

    def with_debt(self):
        return self.get_queryset().with_debt()

    def with_balance(self):
        return self.get_queryset().with_balance()

    def with_related(self):
        return self.get_queryset().with_related()