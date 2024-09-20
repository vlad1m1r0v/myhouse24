# Generated by Django 5.1 on 2024-09-19 12:22

import src.core.utils.media
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0004_aboutusdocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicesPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seo_title', models.CharField()),
                ('seo_keywords', models.CharField()),
                ('seo_description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServicesPageBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=src.core.utils.media.get_upload_path)),
                ('title', models.CharField()),
                ('description', models.TextField()),
            ],
        ),
    ]