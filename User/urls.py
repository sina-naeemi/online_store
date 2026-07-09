from django.contrib import admin
from django.urls import path

from .views import UserRegister , GetToken

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns=[
    path("account/enter/" , UserRegister.as_view()) , 
    path("verify-otp/" , GetToken.as_view()),
    # path('َusers/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh') #هنگامی که توکن منقضی شد با این ،یک جدیدش ایجاد میشه
]