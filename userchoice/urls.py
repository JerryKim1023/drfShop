from django.urls import path
from . import views

urlpatterns = [
	path('cart/', views.CartView.as_view(), name="cart_view"), # cart
	path('cart/<obj_id>/', views.CartView.as_view(), name="cart_view"), # cart ReviewView
	path('review/', views.ReviewView.as_view(), name="review"), # review
	path('review/<obj_id>/', views.ReviewView.as_view(), name="review"), # review
	path('like/<obj_id>/', views.LikeView.as_view(), name="like"), # like
	path('order-list/', views.OrderListView.as_view(), name="order_list_view"), # order_list
	path('order-list/<obj_id>/', views.OrderListView.as_view(), name="order_list_view"), # order_list

]