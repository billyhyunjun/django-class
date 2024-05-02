from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer


class UserListAPIView(APIView):
    def post(self, request):
        # validate data
        data = request.data
        email = data.get("email")
        username = data.get("username")

        if not email or not username:
            return Response({"error": "email or username is required"}, status=400)

        if get_user_model().objects.filter(email=email).exists():
            return Response({"error": "email exists"}, status=400)

        if get_user_model().objects.filter(username=username).exists():
            return Response({"error": "username exists"}, status=400)

        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=data.get("password"),
            gender=data.get("gender"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            birthdate=data.get("birthdate"),
        )
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            status=201,
        )

    def delete(self, request):
        password = request.data.get("password")
        if not password:
            return Response({"error": "password is required"}, status=400)

        if not request.user.check_password(password):
            return Response({"error": "password is incorrect"}, status=400)

        request.user.delete()
        return Response(status=204)


class UserDetailAPIView(APIView):
    def get(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        # 1. get user
        user = get_object_or_404(get_user_model(), username=username)

        # 2. check if request user is the same as the user
        if request.user != user:
            return Response({"error": "permission denied"}, status=403)

        # 3. update user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 4. return user using serializer
        return Response(serializer.data)


class ChangePasswordAPIView(APIView):
    def put(self, request):
        user = request.user
        password = request.data.get("password")
        if not password:
            return Response({"error": "password is required"}, status=400)

        if len(password) < 8:
            return Response(
                {"error": "password must be at least 8 characters"}, status=400
            )

        user.set_password(password)
        user.save()
        return Response(status=204)
