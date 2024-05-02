from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.SignupAPIView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("<str:username>/", views.UserDetailAPIView.as_view(), name="user-detail"),
]
