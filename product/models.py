from django.db import models

from user.models import User as UserModel


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
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    title = models.CharField("상품명", max_length=40)
    thumbnail = models.ImageField("썸네일", upload_to="product/thumbnail",  height_field=None, width_field=None, max_length=None)
    desc = models.TextField("설명", blank=True)
    created = models.DateTimeField("등록시간", auto_now_add=True)
    modified = models.DateTimeField("수정시간", auto_now=True)
    show_expired_date = models.DateField("노출 종료일", (""),auto_now=False, auto_now_add=False) # 노출 종료일

    stock = models.IntegerField("재고")
    product_like = models.ManyToManyField("product.Like", verbose_name="좋아요")

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


# Create your models here.
class Review(models.Model):
    class Meta:
        db_table = "review"
    # <작성자, 상품, 내용, 평점, 작성일>
    user = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField("평점", blank=True)
    product = models.ForeignKey(Product, verbose_name="상품", on_delete=models.SET_NULL, null=True)
    content = models.TextField("내용", blank=True)
    created = models.DateTimeField("등록시간", auto_now_add=True)
    

    def __str__(self):
        return f"{self.product} {self.user} 댓글 : {self.content} 입니다"

class Like(models.Model):
    class Meta:
        db_table = "like"
    # <작성자, 상품, 내용, 평점, 작성일>
    user = models.ForeignKey("user.User", verbose_name="작성자", on_delete=models.SET_NULL, null=True)
    product_like = models.ForeignKey(Product, verbose_name="상품", on_delete=models.SET_NULL, null=True)
    
    # like_date(mtm 활용 가능)??

    def __str__(self):
        return f"{self.product_like.title}은 {self.user}님이 좋아요한 상품입니다"


class Cart(models.Model):
    class Meta:
        db_table = "cart"

    user = models.ForeignKey("user.User", verbose_name="고객", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name="상품", on_delete=models.SET_NULL, null=True)
    product_option = models.ForeignKey(ProductOption, verbose_name="상품옵션", on_delete=models.SET_NULL, null=True)
    is_paid = models.BooleanField("지불여부", default=False)

    def __str__(self):
        return f"{self.product}이 담겨져 있습니다."


class OrderList(models.Model):
    PayCheck = [
        ('현금', '현금'), ('카드', '카드'),('계좌이체', '계좌이체')
    ]

    DELIVERY_STATE = [
        ('배송준비 중', u'배송준비 중'),
        ('배송 중', u'배송 중'),
        ('배송완료', u'배송완료')
    ]
    user = models.ForeignKey("user.User", verbose_name="고객", on_delete=models.SET_NULL, null=True)
    cart = models.ManyToManyField(to="Cart", verbose_name="장바구니")
    the_time_payed = models.DateTimeField("구매완료 시간", auto_now_add=True)
    # complete = models.BooleanField("주문완료", default=True)
    pay_check = models.CharField(verbose_name='결제방식', max_length=4, choices=PayCheck, default='')

    delivery_state = models.CharField(u'배송상태', max_length=50, default='배송준비 중', choices=DELIVERY_STATE)

    def __str__(self):
        return f"{self.the_time_payed}에 주문 완료되었습니다."
    
	# @property
	# def get_total(self):
	# 	total = self.product_option.price * self.product_option.quantity
	# 	return total



    