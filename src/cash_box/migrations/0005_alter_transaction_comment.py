# Generated by Django 5.1.5 on 2025-04-09 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash_box', '0004_transaction_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
