# Generated by Django 4.0.5 on 2022-07-04 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userchoice', '0004_orderlist_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='customer',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='orderlist',
            old_name='customer',
            new_name='user',
        ),
    ]
