from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "birthdate",
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if "email" in attrs:
            if get_user_model().objects.filter(email=attrs["email"]).exists():
                raise serializers.ValidationError("email exists")

        if "username" in attrs:
            if get_user_model().objects.filter(username=attrs["username"]).exists():
                raise serializers.ValidationError("username exists")

        return attrs
