"""drfShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import include, path

from drfShop import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'drfShop'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_main_page, name='show_mainpage'),
    path('user/', include("user.urls"), name='user_view'),
    path('userchoice/', include("userchoice.urls"), name='userchoice_view'),
    path('product/', include("product.urls"), name='product_view'),

    path('login/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('jwt-token-auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt-token-auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
