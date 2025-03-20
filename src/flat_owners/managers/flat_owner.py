from django.db import models
from django.db.models import Exists, OuterRef, Value, F
from django.db.models.functions import Concat

from src.payment_receipts.models import Receipt


class FlatOwnerQuerySet(models.QuerySet):
    def with_debt(self):
        return self.annotate(
            has_debt=Exists(
                Receipt.objects.filter(
                    flat__owner=OuterRef("pk"),
                    status__in=["unpaid", "partially_paid"]
                )
            )
        )

    def with_full_name(self):
        return self.annotate(
            full_name=Concat(
                F("last_name"), Value(" "),
                F("first_name"), Value(" "),
                F("middle_name")
            )
        )

class FlatOwnerManager(models.Manager):
    def get_queryset(self):
        return FlatOwnerQuerySet(self.model, using=self._db)

    def with_debt(self):
        return self.get_queryset().with_debt()

    def with_full_name(self):
        return self.get_queryset().with_full_name()