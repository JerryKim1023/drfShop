# Generated by Django 4.0.5 on 2022-06-24 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersellerprofile',
            name='interests',
        ),
        migrations.RemoveField(
            model_name='usersellerprofile',
            name='user',
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=20, unique=True, verbose_name='사용자 계정'),
        ),
        migrations.DeleteModel(
            name='UserSeller',
        ),
        migrations.DeleteModel(
            name='UserSellerProfile',
        ),
    ]
