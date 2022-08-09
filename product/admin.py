from django.contrib import admin
from product.models import Product as ProductModel
from product.models import ProductOption as ProductOptionModel
from product.models import Category as CategoryModel

from .models import Review as ReviewModel
from .models import Like as LikeModel
from .models import Cart as CartModel
from .models import OrderList as OrderListModel

from django.utils.safestring import mark_safe

class ProductOptionInline(admin.StackedInline): # 세로로 뿌려줌
    model = ProductOptionModel

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title", 
        # "thumbnail",
        "category",
        "title",
        "desc",
        "created",
        "modified",
        "show_expired_date",
        "stock",
        "is_active",

        "thumbnail_preview",
    )
    readonly_fields = ('product_like', )
    def thumbnail_preview(self, obj):
        return mark_safe(f'<img src="/product/thumbnail/{obj.id}/" height="100px"/>')

    thumbnail_preview.short_decription = "Thumbnail"

    inlines = (
            ProductOptionInline,
        )

class ProductOptionAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "options", 
        "quantity",
        "sizes",
        "price",
    )

admin.site.register(ProductModel, ProductAdmin)
# admin.site.register(ProductOptionModel, ProductOptionAdmin)
admin.site.register(CategoryModel)


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