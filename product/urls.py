from django.urls import path

from product.views.cart import CartListCreateAPI, CartDetailAPI
from product.views.category import CategoryListCreateAPI, CategoryDetailAPI
from product.views.like import LikeAPI
from product.views.order import OrderListCreateAPI, OrderDetailAPI
from product.views.product import ProductListCreateAPI, ProductDetailAPI, ProductThumbnailView
from product.views.review import ReviewByProduct, ReviewWrite, ReviewChangeDelete




urlpatterns = [
	# Cart
    path("categories", CartListCreateAPI.as_view()),
    path("categories/<int:id>", CartDetailAPI.as_view()),

	# Category
	path('category/', CategoryListCreateAPI.as_view(), name="category_view"), # 카테고리
	path('category/<int:id>', CategoryDetailAPI.as_view(), name="category_view"), # 카테고리

	# Like
	path('like/<int:id>', LikeAPI.as_view(), name="like"), # like

	# Order
	path('order-list/', OrderListCreateAPI.as_view(), name="order_list_view"), # order_list
	path('order-list/<int:id>', OrderDetailAPI.as_view(), name="order_list_view"), # order_list

	# Product
	path('sell/', ProductListCreateAPI.as_view(), name="product_item_view"), # 상품 조회
	path('sell/<int:id>', ProductDetailAPI.as_view(), name="product_item_view"), # 상품 상세보기

	# 리뷰 Review
	path('review/<int:id>', ReviewByProduct.as_view(), name="review"), # 상품별 review 조회 / 상품 id 받아옴
	path('review/<int:id>', ReviewWrite.as_view(), name="review"), # 1 review 작성 / 상품 id 받아옴
	path('review/<int:id>', ReviewChangeDelete.as_view(), name="review"), # 2 review 수정,삭제 / 댓글 id 받아옴

	# Product_thumbnail
	path('thumbnail/<obj_id>', ProductThumbnailView.as_view(), name='thumbnail_view'), # 어드민용 썸네일뷰 함수

]
