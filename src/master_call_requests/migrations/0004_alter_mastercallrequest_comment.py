# Generated by Django 5.1.5 on 2025-04-03 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_call_requests', '0003_alter_mastercallrequest_master'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mastercallrequest',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
