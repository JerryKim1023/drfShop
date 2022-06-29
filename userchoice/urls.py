from django.urls import path
from . import views

urlpatterns = [
	path('cart/', views.CartView.as_view(), name="cart_view"), # cart
	path('cart/<obj_id>/', views.CartView.as_view(), name="cart_view"), # cart
	# path('login/', views.UserLoginView.as_view(), name="user_api_view"), # login 등 user의 기본적인 api담당
	# path('seller/<obj_id>/', views.UserSellerApiView.as_view(), name="user_api_view"), # signup, login 등 user의 기본적인 api담당

]