from django.db import models

from src.houses.models import House, HouseSection
from src.system_settings.models import Service


class StatusChoices(models.TextChoices):
    NEW = 'new', 'Нове'
    ACCOUNTED = 'accounted', 'Враховано'
    ACCOUNTED_AND_PAID = 'accounted_paid', 'Враховано та оплачено'
    ZERO = 'zero', 'Нульове'


# Create your models here.
class MeterIndicator(models.Model):
    no = models.CharField(max_length=20)
    date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW,
    )
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    section = models.ForeignKey(HouseSection, on_delete=models.CASCADE)
    flat = models.ForeignKey('flats.Flat', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return f"Показник № {self.no}"
