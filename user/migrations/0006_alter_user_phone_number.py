# Generated by Django 4.0.5 on 2022-06-28 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=30, verbose_name='전화번호'),
        ),
    ]
