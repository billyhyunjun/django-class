from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # def get(self, request):
    #     products = Product.objects.all()
    #     serializer = ProductSerializer(products, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        name = request.data.get("name")
        context = request.data.get("context")
        image = request.data.get("image")

        # validate data
        if not (name and context and image):
            return Response({"error": "name, context, image is required"}, status=400)

        # save data
        product = Product.objects.create(
            name=name,
            context=context,
            image=image,
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

        # serialize product
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def delete(self, request, pk):
        # 1. get product
        product = get_object_or_404(Product, pk=pk)
        # 2. check if user is owner
        if product.user != request.user:
            return Response(
                {"error": "You don't have permission to delete this product"},
                status=400,
            )
        # 3. delete product
        product.delete()
        # 4. return success message
        return Response(status=204)
