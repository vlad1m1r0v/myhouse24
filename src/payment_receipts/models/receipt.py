from django.db import models

from src.houses.models import House, HouseSection
from src.meter_indicators.models import MeterIndicator
from src.system_settings.models import (
    Tariff,
    Service,
    MeasurementUnit
)

STATUS_CHOICES = [
    ("unpaid", "неоплачена"),
    ("partially_paid", "частково оплачена"),
    ("paid", "оплачена"),
]


# Create your models here.
class Receipt(models.Model):
    no = models.CharField(max_length=20)
    date = models.DateField()
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    section = models.ForeignKey(HouseSection, on_delete=models.CASCADE)
    flat = models.ForeignKey('flats.Flat', on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    period_from = models.DateField()
    period_to = models.DateField()
    is_complete = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, default="unpaid")
    personal_account = models.ForeignKey("personal_accounts.PersonalAccount", on_delete=models.CASCADE,
                                         related_name="account_receipts")

    def __str__(self):
        return f"Квитанція № {self.no}"


class ReceiptService(models.Model):
    meter_indicator = models.OneToOneField(MeterIndicator, null=True, blank=True, on_delete=models.CASCADE,
                                           related_name='receipt_service')
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name="services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=1)
    value = models.FloatField()
