# Generated by Django 4.0.5 on 2022-07-05 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userchoice', '0005_rename_customer_cart_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlist',
            name='complete',
        ),
        migrations.AddField(
            model_name='cart',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='지불여부'),
        ),
    ]