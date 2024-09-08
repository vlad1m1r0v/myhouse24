# Generated by Django 5.1 on 2024-09-08 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_settings', '0005_remove_tariff_services_tariffservice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tariffservice',
            name='tariff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='system_settings.tariff'),
        ),
    ]