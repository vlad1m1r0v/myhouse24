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
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    section = models.ForeignKey(HouseSection, on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, null=True, blank=True, on_delete=models.CASCADE)