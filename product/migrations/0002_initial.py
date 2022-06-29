# Generated by Django 4.0.5 on 2022-06-28 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userchoice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_like',
            field=models.ManyToManyField(to='userchoice.like', verbose_name='좋아요'),
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='작성자'),
        ),
    ]
