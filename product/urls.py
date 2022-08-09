from django.urls import path

from product.views.cart import CartView
from product.views.category import CategoryView
from product.views.like import LikeView
from product.views.order import OrderListView
from product.views.product import ProductItemView, ProductThumbnailView
from product.views.review import ReviewView





urlpatterns = [
	# Cart
	path('cart/', CartView.as_view(), name="cart_view"), # cart
	path('cart/<obj_id>/', CartView.as_view(), name="cart_view"), # cart ReviewView

	# Category
	path('category/', CategoryView.as_view(), name="category_view"), # 카테고리
	path('category/<obj_id>/', CategoryView.as_view(), name="category_view"), # 카테고리

	# Like
	path('like/<obj_id>/', LikeView.as_view(), name="like"), # like

	# Order
	path('order-list/', OrderListView.as_view(), name="order_list_view"), # order_list
	path('order-list/<obj_id>/', OrderListView.as_view(), name="order_list_view"), # order_list

	# Product
	path('sell/', ProductItemView.as_view(), name="product_item_view"), # 모든 상품에 대한 조회, 생성 등 product의 기본적인 api담당
	path('sell/<obj_id>/', ProductItemView.as_view(), name="product_item_view"), # 모든 상품에 대한 수정, 삭제 등 user의 기본적인 api담당

	# Review
	path('review/', ReviewView.as_view(), name="review"), # review
	path('review/<obj_id>/', ReviewView.as_view(), name="review"), # review

	# Product_thumbnail
	path('thumbnail/<obj_id>/', ProductThumbnailView.as_view(), name='thumbnail_view'),

]
