from django.contrib.auth.models import Group, Permission
from django.db import models

TYPE_CHOICES = [
    ('income', 'прихід'),
    ('expense', 'витрата')
]


class PaymentItem(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, null=False)

class PaymentCredential(models.Model):
    name = models.CharField(max_length=50)
    information = models.TextField()


class GroupPermissionProxy(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'