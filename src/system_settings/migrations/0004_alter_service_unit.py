# Generated by Django 5.1 on 2024-09-06 18:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_settings', '0003_measurementunit_service_tariff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='system_settings.measurementunit'),
        ),
    ]
