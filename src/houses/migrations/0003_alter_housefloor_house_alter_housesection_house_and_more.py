# Generated by Django 5.1 on 2024-09-30 13:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0002_remove_house_user_houseuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housefloor',
            name='house',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='floors', to='houses.house'),
        ),
        migrations.AlterField(
            model_name='housesection',
            name='house',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='houses.house'),
        ),
        migrations.AlterField(
            model_name='houseuser',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='houses.house'),
        ),
    ]