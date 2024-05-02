from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from django.db.models import Q
from .models import Product, Category
from .serializers import ProductSerializer


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        query_params = self.request.query_params
        name = query_params.get("name")
        context = query_params.get("context")
        username = query_params.get("username")

        q = Q()
        if name:
            q &= Q(name__icontains=name)
        if context:
            q &= Q(context__icontains=context)
        if username:
            q &= Q(user__username=username)

        return Product.objects.filter(q)

    def post(self, request):
        name = request.data.get("name")
        context = request.data.get("context")
        image = request.data.get("image")
        category = request.data.get("category")

        # validate data
        if not (name and context and image):
            return Response({"error": "name, context, image is required"}, status=400)

        if category:
            category = get_object_or_404(Category, pk=category)

        # save data
        product = Product.objects.create(
            user=request.user,
            name=name,
            context=context,
            image=image,
            category=category,
        )

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=201)


class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if product.user != request.user:
            return Response(
                {"error": "You don't have permission to edit this product"},
                status=400,
            )

        name = request.data.get("name", product.name)
        context = request.data.get("context", product.context)
        image = request.data.get("image", product.image)

        # update product
        product.name = name
        product.context = context
        product.image = image
        product.save()

        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.user != request.user:
            return Response(
                {"error": "You don't have permission to delete this product"},
                status=400,
            )
        product.delete()
        return Response(status=204)


class CategoryListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        name = request.data.get("name")
        if not name:
            return Response({"error": "name is required"}, status=400)

        category, _ = Category.objects.get_or_create(name=name)
        return Response({"id": category.id, "name": category.name})
