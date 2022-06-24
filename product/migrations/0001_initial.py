# Generated by Django 4.0.5 on 2022-06-24 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='상품명')),
                ('thumbnail', models.ImageField(upload_to='product/thumbnail', verbose_name='썸네일')),
                ('desc', models.TextField(blank=True, verbose_name='설명')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='등록시간')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='수정시간')),
                ('show_expired_date', models.DateField(verbose_name='노출 종료일')),
                ('stock', models.IntegerField(verbose_name='재고')),
                ('is_active', models.BooleanField(default=True, verbose_name='활성화 여부')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='ProductOption',
            fields=[
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='product.product', verbose_name='상품')),
                ('name', models.CharField(max_length=50, verbose_name='상품옵션이름')),
                ('quantity', models.IntegerField(verbose_name='수량')),
                ('size', models.CharField(max_length=10, verbose_name='사이즈')),
                ('price', models.IntegerField(verbose_name='가격')),
            ],
            options={
                'db_table': 'product_option',
            },
        ),
    ]