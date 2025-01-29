from django.db import models

from src.authentication.models import CustomUser
from src.core.utils import get_upload_path


class House(models.Model):
    name = models.CharField()
    address = models.TextField()
    image_1 = models.ImageField(upload_to=get_upload_path)
    image_2 = models.ImageField(upload_to=get_upload_path)
    image_3 = models.ImageField(upload_to=get_upload_path)
    image_4 = models.ImageField(upload_to=get_upload_path)
    image_5 = models.ImageField(upload_to=get_upload_path)

    def __str__(self):
        return self.name


class HouseUser(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='users')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)


class HouseFloor(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='floors')
    name = models.CharField()

class HouseSection(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField()

    def __str__(self):
        return self.name
