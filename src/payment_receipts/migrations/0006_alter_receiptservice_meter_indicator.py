# Generated by Django 5.1.5 on 2025-03-20 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meter_indicators', '0002_rename_countermeasurement_meterindicator'),
        ('payment_receipts', '0005_alter_receipt_personal_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receiptservice',
            name='meter_indicator',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receipt_service', to='meter_indicators.meterindicator'),
        ),
    ]
