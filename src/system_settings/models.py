from django.contrib.auth.models import Group, Permission
from django.db import models

TYPE_CHOICES = [
    ('income', 'прихід'),
    ('expense', 'витрата')
]


class PaymentItem(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, null=False)

class PaymentCredential(models.Model):
    name = models.CharField(max_length=50)
    information = models.TextField()

class MeasurementUnit(models.Model):
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.unit

class Service(models.Model):
    name = models.CharField(max_length=50)
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE, related_name='services')
    show_in_counters = models.BooleanField(default=False)

class Tariff(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)


class TariffService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE,)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, related_name='services')
    price = models.DecimalField(max_digits=6, decimal_places=2)


