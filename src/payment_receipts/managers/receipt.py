from django.db import models
from django.db.models import Sum, F, FloatField


class ReceiptQuerySet(models.QuerySet):
    def with_total_price(self):
        return self.prefetch_related("services").annotate(
            total_price=Sum(F("services__price") * F("services__value"), output_field=FloatField())
        )


class ReceiptManager(models.Manager):
    def get_queryset(self):
        return ReceiptQuerySet(self.model, using=self._db)

    def with_total_price(self):
        return self.get_queryset().with_total_price()
