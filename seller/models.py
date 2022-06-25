from ctypes import sizeof
from django.db import models

from product.models import ProductOption as ProductOptionModel

# Create your models here.

class Option(models.Model):
    class Meta:
        db_table = "product_option_name"
        
    product_options = models.OneToOneField(ProductOptionModel, on_delete=models.CASCADE, unique=True)
    option_name = models.CharField(max_length=50)

    def __str__(self):
        return self.option_name

class Size(models.Model):
    class Meta:
        db_table = "product_option_size"
    product_options = models.OneToOneField(ProductOptionModel, on_delete=models.CASCADE, unique=True)
    size_name = models.CharField(max_length=50)

    def __str__(self):
        return self.size_name