from django.contrib import admin

from seller.models import Option as OptionModel
from seller.models import Size as SizeModel


# Register your models here.


admin.site.register(OptionModel)
admin.site.register(SizeModel)