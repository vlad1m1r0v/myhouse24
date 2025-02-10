from django.db import models

from src.flats.models import Flat
from src.houses.models import House, HouseSection

STATUS_CHOICES = [
    ("active", "активний"),
    ("disabled", "деактивований"),
]


# Create your models here.
class PersonalAccount(models.Model):
    no = models.CharField(max_length=20)
    status = models.CharField(choices=STATUS_CHOICES, default="active")
    house = models.ForeignKey(House, null=True, blank=True, on_delete=models.CASCADE)
    section = models.ForeignKey(HouseSection, null=True, blank=True, on_delete=models.CASCADE)
    flat = models.OneToOneField(Flat, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Особовий рахунок № {self.no}"