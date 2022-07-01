from django.contrib import admin

from .models import Review as ReviewModel
from .models import Like as LikeModel
from .models import Cart as CartModel


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'rating', 'content')
# Register your models here.
admin.site.register(LikeModel)
admin.site.register(ReviewModel, ReviewAdmin)
admin.site.register(CartModel)