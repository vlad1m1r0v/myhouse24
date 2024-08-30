# Generated by Django 5.1 on 2024-08-28 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_customuser_options_alter_customuser_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('statistics', 'статистика'), ('cash_box', 'каса'), ('receipts', 'квитанції на оплату'), ('personal_accounts', 'особові рахунки'), ('flats', 'квартири'), ('flat_owners', 'власники квартир'), ('houses', 'будинки'), ('messages', 'повідомлення'), ('service_call_requests', 'заявки виклику майстра'), ('meter_indicators', 'показники лічильників'), ('website_management', 'управління сайтом'), ('services', 'послуги'), ('tariffs', 'тарифи'), ('roles', 'ролі'), ('users', 'користувачі'), ('payment_information', 'платіжні реквізити'), ('payment_items', 'статті платежів')]},
        ),
    ]
