from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status
from django.contrib.auth.models import User

from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsUserOrAdmin


#? Регистрация нового пользователя
class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        telegram_chat_id = request.data.get('telegram_chat_id')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if telegram_chat_id:
                user.telegram_chat_id = telegram_chat_id
                user.save()
            return Response({"message": "User created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#? Авторизация пользователя
class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email,
                'id': user.id,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#? Выход пользователя из системы (Только для аутентифицированных)
class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


#? Список всех пользователей (Только для админов)
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (JWTAuthentication,)


#? Детальная информация о пользователе
class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated, IsUserOrAdmin)
    authentication_classes = (JWTAuthentication,)


#? Обновление информации пользователя
class UserUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, IsUserOrAdmin)
    authentication_classes = (JWTAuthentication,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        if not self.request.user.is_staff and self.request.user != serializer.instance:
            raise PermissionDenied('You are not allowed to update this user')
        serializer.save()


#? Удаление пользователя (только для админов)
class UserDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (JWTAuthentication,)

    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def perform_destroy(self, instance):
        if not self.request.user.is_staff and self.request.user != instance:
            raise PermissionDenied('You are not allowed to delete this user')
        instance.delete()
