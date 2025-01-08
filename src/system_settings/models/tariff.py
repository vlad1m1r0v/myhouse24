from django.db import models

from src.system_settings.models.service import Service


class Tariff(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)


class TariffService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE,)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, related_name='services')
    price = models.DecimalField(max_digits=6, decimal_places=1)