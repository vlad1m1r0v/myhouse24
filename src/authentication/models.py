from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager
STATUS_CHOICES = [
    ("new", "новий"),
    ("active", "активний"),
    ("disabled", "деактивований"),
]

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None

    ID = models.PositiveIntegerField(unique=True, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    telegram = models.CharField(max_length=50, null=True, blank=True)
    viber = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    about_me = models.TextField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        permissions = [
            ('statistics', 'статистика'),
            ('cash_box', 'каса'),
            ('receipts', 'квитанції на оплату'),
            ('personal_accounts', 'особові рахунки'),
            ('flats', 'квартири'),
            ('flat_owners', 'власники квартир'),
            ('houses', 'будинки'),
            ('messages', 'повідомлення'),
            ('service_call_requests', 'заявки виклику майстра'),
            ('meter_indicators', 'показники лічильників'),
            ('website_management', 'управління сайтом'),
            ('services', 'послуги'),
            ('tariffs', 'тарифи'),
            ('roles', 'ролі'),
            ('users', 'користувачі'),
            ('payment_information', 'платіжні реквізити'),
            ('payment_items', 'статті платежів')
        ]
