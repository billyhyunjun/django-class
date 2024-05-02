from django.shortcuts import render
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
