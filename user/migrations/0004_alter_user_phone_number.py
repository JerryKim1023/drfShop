# Generated by Django 4.0.5 on 2022-06-24 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=30, unique=True, verbose_name='전화번호'),
        ),
    ]
