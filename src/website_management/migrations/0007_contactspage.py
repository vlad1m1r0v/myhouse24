# Generated by Django 5.1 on 2024-09-20 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0006_tariffspage_tariffspageblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactsPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seo_title', models.CharField()),
                ('seo_keywords', models.CharField()),
                ('seo_description', models.TextField()),
                ('title', models.CharField()),
                ('description', models.TextField()),
                ('website_link', models.URLField()),
                ('map_iframe', models.TextField()),
                ('name', models.CharField()),
                ('location', models.CharField()),
                ('address', models.CharField()),
                ('phone', models.CharField()),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
