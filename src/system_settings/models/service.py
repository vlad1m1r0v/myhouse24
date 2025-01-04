from django.db import models


class MeasurementUnit(models.Model):
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.unit

class Service(models.Model):
    name = models.CharField(max_length=50)
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE, related_name='services')
    show_in_counters = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} ({self.unit})'