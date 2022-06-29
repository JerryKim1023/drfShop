from django.db import models


import userchoice
# from userchoice.models import Like as LikeModel

# Create your models here.
class Category(models.Model):
    class Meta:
        db_table = "category"

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        db_table = "product"
    # <제목, 썸네일, 설명, 등록일자, 노출 시작 일, 노출 종료일, 활성화 여부>
    user = models.ForeignKey("user.User", verbose_name="작성자", on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField("상품명", max_length=40)
    thumbnail = models.ImageField("썸네일", upload_to="product/thumbnail",  height_field=None, width_field=None, max_length=None)
    desc = models.TextField("설명", blank=True)
    created = models.DateTimeField("등록시간", auto_now_add=True)
    modified = models.DateTimeField("수정시간", auto_now=True)
    show_expired_date = models.DateField("노출 종료일", (""),auto_now=False, auto_now_add=False) # 노출 종료일

    stock = models.IntegerField("재고")
    product_like = models.ManyToManyField('userchoice.Like', verbose_name="좋아요")

    is_active = models.BooleanField("활성화 여부", default=True)  # 활성화 여부

    

    def __str__(self):
        return f"{self.title} 입니다"

class ProductOption(models.Model):
    class Meta:
        db_table = "product_option"

    product = models.OneToOneField(to=Product, verbose_name="상품", on_delete=models.CASCADE, primary_key=True)
    options = models.CharField("옵션", max_length=50)
    quantity = models.IntegerField("수량")
    sizes = models.CharField("사이즈", max_length=10)
    price = models.IntegerField("가격")

    def __str__(self):
        return self.options





    