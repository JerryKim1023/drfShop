from django.db import models

from product.models import Product as ProductModel  
from product.models import ProductOption as ProductOptionModel
from user.models import User as UserModel

# Create your models here.
class Review(models.Model):
    class Meta:
        db_table = "review"
    # <작성자, 상품, 내용, 평점, 작성일>
    user = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField("평점", blank=True)
    product = models.ForeignKey(ProductModel, verbose_name="상품", on_delete=models.SET_NULL, null=True)
    content = models.TextField("내용", blank=True)
    created = models.DateTimeField("등록시간", auto_now_add=True)
    

    def __str__(self):
        return f"{self.product} {self.user} 댓글 : {self.content} 입니다"

class Like(models.Model):
    class Meta:
        db_table = "like"
    # <작성자, 상품, 내용, 평점, 작성일>
    user = models.ForeignKey("user.User", verbose_name="작성자", on_delete=models.SET_NULL, null=True)
    product_like = models.ForeignKey(ProductModel, verbose_name="상품", on_delete=models.SET_NULL, null=True)
    
    # like_date(mtm 활용 가능)??

    def __str__(self):
        return f"{self.product_like.title}은 {self.user}님이 좋아요한 상품입니다"


class Cart(models.Model):
    class Meta:
        db_table = "cart"

    customer = models.ForeignKey("user.User", verbose_name="고객", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(ProductModel, verbose_name="상품", on_delete=models.SET_NULL, null=True)
    product_option = models.ForeignKey(ProductOptionModel, verbose_name="상품옵션", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.product.title}이 담겨져 있습니다."


class Order(models.Model):

    class Meta:
        db_table = "order_list"

    PayCheck = (
        ('현금', '현금'), ('카드', '카드'),('계좌이체', '계좌이체')
    )

    DELIVERY_STATE = [
        ('배송준비 중', u'배송준비 중'),
        ('배송 중', u'배송 중'),
        ('배송완료', u'배송완료')
    ]
    cart = models.ForeignKey(Cart, verbose_name="장바구니", on_delete=models.SET_NULL, null=True)
    complete = models.BooleanField("주문완료", default=False)
    pay_check = models.CharField(verbose_name='결제방식', max_length=4, choices=PayCheck, default='')

    delivery_state = models.CharField(u'배송상태', max_length=50, default='배송준비 중', choices=DELIVERY_STATE)


    def __str__(self):
        return str(self.id)

    # @property
    # def get_cart_total(self):
    #     orderitems = self.orderitem_set.all()
    #     total = sum([item.get_total for item in orderitems])
    #     return total 

    # @property
    # def get_cart_items(self):
    #     orderitems = self.orderitem_set.all()
    #     total = sum([item.quantity for item in orderitems])
    #     return total 

class OrderList(models.Model):
	order = models.ForeignKey("주문", Order, on_delete=models.SET_NULL, null=True)
	the_time_payed = models.DateTimeField("구매완료 시간", auto_now_add=True)

	@property
	def get_total(self):
		total = self.product_option.price * self.product_option.quantity
		return total