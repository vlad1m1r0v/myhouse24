from django.db import models

from src.authentication.models import CustomUser
from src.flats.models import Flat
from src.houses.models import House, HouseSection, HouseFloor


class Message(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topic = models.CharField()
    description = models.TextField()
    to_debtors = models.BooleanField(default=False)
    house = models.ForeignKey(House, null=True, blank=True, on_delete=models.CASCADE)
    section = models.ForeignKey(HouseSection, null=True, blank=True, on_delete=models.CASCADE)
    floor = models.ForeignKey(HouseFloor, null=True, blank=True, on_delete=models.CASCADE)
    flat = models.OneToOneField(Flat, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ReadMessage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
