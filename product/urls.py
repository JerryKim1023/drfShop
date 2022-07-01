from django.urls import path
from . import views

urlpatterns = [
	path('sell/', views.ProductItemView.as_view(), name="product_item_view"), # 모든 상품에 대한 조회, 생성 등 product의 기본적인 api담당
	path('sell/<obj_id>/', views.ProductItemView.as_view(), name="product_item_view"), # 모든 상품에 대한 수정, 삭제 등 user의 기본적인 api담당
	path('category/', views.CategoryView.as_view(), name="category_view"), # 카테고리
	path('category/<obj_id>/', views.CategoryView.as_view(), name="category_view"), # 카테고리
	path('thumbnail/<obj_id>/', views.ProductThumbnailView.as_view(), name='thumbnail_view'),

	
]