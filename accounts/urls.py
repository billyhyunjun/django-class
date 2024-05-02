from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.SignupAPIView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("password/", views.ChangePasswordAPIView.as_view(), name="change_password"),
    path("<str:username>/", views.UserDetailAPIView.as_view(), name="user-detail"),
]
