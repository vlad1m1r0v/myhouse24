from django.db import models


class PaymentCredential(models.Model):
    name = models.CharField(max_length=50)
    information = models.TextField()