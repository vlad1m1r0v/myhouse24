from django.db import models

TYPE_CHOICES = [
    ('income', 'прихід'),
    ('expense', 'витрата')
]


class PaymentItem(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, null=False)

    def __str__(self):
        return self.name