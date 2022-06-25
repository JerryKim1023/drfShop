from django.db import models

from product.models import Product as ProductModel

# Create your models here.
class Review(models.Model):
    class Meta:
        db_table = "review"
    # <작성자, 상품, 내용, 평점, 작성일>
    user = models.ForeignKey("user.User", verbose_name="작성자", on_delete=models.SET_NULL, null=True)
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
        return f"{self.product}은 {self.user}님이 좋아요한 상품입니다"


class Cart(models.Model):
    class Meta:
        db_table = "cart"

    PayCheck = (
        ('현금', '현금'), ('카드', '카드'),('계좌이체', '계좌이체')
    )

    user = models.ForeignKey("user.User", verbose_name="작성자", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(ProductModel, verbose_name="상품", on_delete=models.SET_NULL, null=True)
    pay_check = models.CharField(verbose_name='결제방식', max_length=4, choices=PayCheck, default='')
    the_time_payed = models.DateTimeField("구매시간", auto_now=True)
    delivery_state = models.CharField(verbose_name='배송상태', max_length=4, default='준비중')
    def __str__(self):
        return f"{self.product.title}이 담겨져 있습니다."