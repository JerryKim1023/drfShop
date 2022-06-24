from django.urls import path
from . import views

urlpatterns = [
	path('', views.ProductItemView.as_view(), name="product_item_view"), # 조회, 생성 등 product의 기본적인 api담당
	path('<obj_id>', views.ProductItemView.as_view(), name="product_item_view"), # 수정, 삭제 등 user의 기본적인 api담당


]