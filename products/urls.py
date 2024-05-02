from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.ProductListAPIView.as_view(), name="product-list"),
    path("<int:pk>/", views.ProductDetailAPIView.as_view(), name="product-detail"),
]
