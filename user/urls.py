from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
	path('signup/', views.SignupAPI.as_view(), name="user_api_view"), # signup
	path('login/', views.LoginAPI.as_view(), name="user_login_view"), # login
	path('logout/', views.LogoutAPI.as_view(), name="user_logout_view"), # logout


	# JWT
	path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]