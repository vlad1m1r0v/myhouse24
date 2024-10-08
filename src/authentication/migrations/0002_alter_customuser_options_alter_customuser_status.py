# Generated by Django 5.1 on 2024-08-28 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('statistics', 'статистика'), ('cash_box', 'каса'), ('receipts', 'квитанції на оплату'), ('personal_accounts', 'особові рахунки'), ('flats', 'квартири'), ('flat_owners', 'власники квартир'), ('houses', 'будинки'), ('messages', 'повідомлення'), ('service_call_requests', 'заявки виклику майстра'), ('meter_indicators', 'показники лічильників'), ('website_management', 'управління сайтом'), ('services', 'послуги'), ('tariffs', 'тарифи'), ('roles', 'ролі'), ('users', 'користувачі'), ('payment_information', 'платіжні реквізити')]},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='status',
            field=models.CharField(choices=[('new', 'новий'), ('active', 'активний'), ('disabled', 'деактивований')], default='new', max_length=10),
        ),
    ]
