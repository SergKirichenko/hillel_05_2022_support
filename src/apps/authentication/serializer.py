from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# from django.contrib.auth import authenticate
# from django.contrib.auth.hashers import make_password

User = get_user_model()


# Register serializer
class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=50, min_length=6)

    class Meta:
        model = User
        fields = ("id", "email", "password", "first_name", "last_name", "age", "phone")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        attrs["username"] = attrs["email"]
        return super().validate(attrs)


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)

        if email is None:
            raise ValidationError("Email adress or mobile phone is required")

        if password is None:
            raise ValidationError("Password is required")

        user = authenticate(username=email, password=password)

        if user is None:
            raise ValidationError("User not found")

        if not user.is_active:
            raise ValidationError("This user is deactivated")

        return attrs


#####################################################################

# DRF_Yasg - Dictionary OPEN_API
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework import serializers, status
# from rest_framework_simplejwt.views import (
#     TokenBlacklistView,
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
# )


# class TokenObtainPairResponseSerializer(serializers.Serializer):
#     access = serializers.CharField()
#     refresh = serializers.CharField()

#     def create(self, validated_data):
#         raise NotImplementedError()

#     def update(self, instance, validated_data):
#         raise NotImplementedError()


# class DecoratedTokenObtainPairView(TokenObtainPairView):
#     @swagger_auto_schema(
#         responses={
#             status.HTTP_200_OK: TokenObtainPairResponseSerializer,
#         }
#     )
#     def post(self, request, *args, **kwargs):
#         return super().post(request, *args, **kwargs)


# class TokenRefreshResponseSerializer(serializers.Serializer):
#     access = serializers.CharField()

#     def create(self, validated_data):
#         raise NotImplementedError()

#     def update(self, instance, validated_data):
#         raise NotImplementedError()


# class DecoratedTokenRefreshView(TokenRefreshView):
#     @swagger_auto_schema(
#         responses={
#             status.HTTP_200_OK: TokenRefreshResponseSerializer,
#         }
#     )
#     def post(self, request, *args, **kwargs):
#         return super().post(request, *args, **kwargs)


# class TokenVerifyResponseSerializer(serializers.Serializer):
#     def create(self, validated_data):
#         raise NotImplementedError()

#     def update(self, instance, validated_data):
#         raise NotImplementedError()


# class DecoratedTokenVerifyView(TokenVerifyView):
#     @swagger_auto_schema(
#         responses={
#             status.HTTP_200_OK: TokenVerifyResponseSerializer,
#         }
#     )
#     def post(self, request, *args, **kwargs):
#         return super().post(request, *args, **kwargs)


# class TokenBlacklistResponseSerializer(serializers.Serializer):
#     def create(self, validated_data):
#         raise NotImplementedError()

#     def update(self, instance, validated_data):
#         raise NotImplementedError()


# class DecoratedTokenBlacklistView(TokenBlacklistView):
#     @swagger_auto_schema(
#         responses={
#             status.HTTP_200_OK: TokenBlacklistResponseSerializer,
#         }
#     )
#     def post(self, request, *args, **kwargs):
#         return super().post(request, *args, **kwargs)
