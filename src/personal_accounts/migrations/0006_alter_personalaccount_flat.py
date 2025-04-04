# Generated by Django 5.1.5 on 2025-03-17 11:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0007_alter_flat_tariff'),
        ('personal_accounts', '0005_alter_personalaccount_flat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalaccount',
            name='flat',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='personal_account', to='flats.flat'),
        ),
    ]
