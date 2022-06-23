from django.urls import path
from user import views

urlpatterns = [
	path('', views.show_page, name="user_view")
]