from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.ProductListAPIView.as_view(), name="product-list"),
]
