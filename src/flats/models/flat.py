from django.db import models

from src.authentication.models import CustomUser
from src.houses.models import House, HouseSection, HouseFloor
from src.system_settings.models import Tariff


# Create your models here.
class Flat(models.Model):
    no = models.PositiveSmallIntegerField()
    area = models.PositiveSmallIntegerField()
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    section = models.ForeignKey(HouseSection, on_delete=models.CASCADE)
    floor = models.ForeignKey(HouseFloor, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.SET_NULL, related_name='flats')
    tariff = models.ForeignKey(Tariff, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Квартира № {self.no}"