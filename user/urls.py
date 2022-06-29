from django.urls import path
from . import views

urlpatterns = [
	path('signup/', views.UserSignupView.as_view(), name="user_api_view"), # 조회,signup  등 user의 기본적인 api담당
	path('signup/<obj_id>/', views.UserSignupView.as_view(), name="user_api_view"), # 수정, 삭제 등 user의 기본적인 api담당
	path('login/', views.UserLoginView.as_view(), name="user_login_view"), # login 등 user의 기본적인 api담당
	# path('seller/<obj_id>/', views.UserSellerApiView.as_view(), name="user_api_view"), # signup, login 등 user의 기본적인 api담당
	path('logout/', views.UserLogoutView.as_view(), name="user_logout_view"), # logout 등 user의 기본적인 api담당

]