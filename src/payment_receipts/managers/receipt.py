from django.db import models
from django.db.models import Sum, F, FloatField, ExpressionWrapper, DecimalField


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


class ReceiptServiceQuerySet(models.QuerySet):
    def with_total_price(self):
        return self.annotate(
            total_price=ExpressionWrapper(
                F('price') * F('value'),
                output_field=FloatField()
            )
        )


class ReceiptServiceManager(models.Manager):
    def get_queryset(self):
        return ReceiptServiceQuerySet(self.model, using=self._db)

    def with_total_price(self):
        return self.get_queryset().with_total_price()
