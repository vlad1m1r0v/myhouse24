# Generated by Django 5.1 on 2024-09-29 11:25

import django.db.models.deletion
import src.core.utils.media
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
                ('address', models.TextField()),
                ('image_1', models.ImageField(upload_to=src.core.utils.media.get_upload_path)),
                ('image_2', models.ImageField(upload_to=src.core.utils.media.get_upload_path)),
                ('image_3', models.ImageField(upload_to=src.core.utils.media.get_upload_path)),
                ('image_4', models.ImageField(upload_to=src.core.utils.media.get_upload_path)),
                ('image_5', models.ImageField(upload_to=src.core.utils.media.get_upload_path)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HouseFloor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
                ('house', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='houses.house')),
            ],
        ),
        migrations.CreateModel(
            name='HouseSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
                ('house', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='houses.house')),
            ],
        ),
    ]
