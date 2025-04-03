from django.contrib.auth.models import Group
from django.db import models

from src.authentication.models import CustomUser
from src.flats.models import Flat

class StatusChoices(models.TextChoices):
    NEW = 'new', 'Нове'
    IN_PROGRESS = 'in_progress', 'В процесі'
    DONE = 'done', 'Зроблено'

# Create your models here.
class MasterCallRequest(models.Model):
    date = models.DateField()
    time = models.TimeField()
    flat_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_requests')
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    master_type = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.NEW,
    )
    master = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='assigned_requests')
    description = models.TextField()
    comment = models.TextField(blank=True, null=True)