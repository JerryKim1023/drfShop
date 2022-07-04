from django.contrib import admin

from .models import Review as ReviewModel
from .models import Like as LikeModel
from .models import Cart as CartModel
from .models import OrderList as OrderListModel


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'rating', 'content')
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user", 
        "product",
        "product_option",
    )
# Register your models here.
admin.site.register(LikeModel)
admin.site.register(ReviewModel, ReviewAdmin)
admin.site.register(CartModel, CartAdmin)
admin.site.register(OrderListModel)