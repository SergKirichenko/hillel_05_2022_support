# from djoser.serializers import TokenCreateSerializer, UserSerializer
from djoser.views import TokenCreateView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializer import (  # LoginSerializer
    RegistrationSerializer,
    UserSerializer,
)


# Register API
class RegistrationApi(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# логин пока не работает
class LoginApi(TokenCreateView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self._action(serializer)

    # def _action(self, serializer):

    #     token = serializer.user
    #     # token_serializer_class = TokenCreateSerializer(token)
    #     data_token = token_serializer_class
    #     return Response(data_token.data, status=status.HTTP_200_OK)
