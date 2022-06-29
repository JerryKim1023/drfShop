from django.contrib import admin
from product.models import Product as ProductModel
from product.models import ProductOption as ProductOptionModel
from product.models import Category as CategoryModel


from django.utils.safestring import mark_safe

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



class ProductOptionAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "options", 
        "quantity",
        "sizes",
        "price",
    )

admin.site.register(ProductModel, ProductAdmin)
admin.site.register(ProductOptionModel, ProductOptionAdmin)
admin.site.register(CategoryModel)