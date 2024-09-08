# Generated by Django 5.1 on 2024-09-08 08:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_settings', '0004_alter_service_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tariff',
            name='services',
        ),
        migrations.CreateModel(
            name='TariffService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_settings.service')),
                ('tariff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_settings.tariff')),
            ],
        ),
    ]