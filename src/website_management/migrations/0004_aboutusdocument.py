# Generated by Django 5.1 on 2024-09-17 16:57

import src.core.utils.media
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0003_aboutusadditionalgallery_aboutusdocument_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ABoutUsDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
                ('file', models.FileField(upload_to=src.core.utils.media.get_upload_path)),
            ],
        ),
    ]