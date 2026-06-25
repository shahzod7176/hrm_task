from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.serializers.employee_serializers import (
    RegisterSerializer,
    RegisterResponseSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset             = User.objects.all()
    serializer_class     = RegisterSerializer
    permission_classes   = (permissions.AllowAny,)

    @extend_schema(
        tags=['auth'],
        summary='Регистрация нового пользователя',
        responses={201: RegisterResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user    = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'user':    {'id': user.id, 'username': user.username, 'email': user.email},
                'access':  str(refresh.access_token),
                'refresh': str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        tags=['auth'],
        summary='Выход из системы (blacklist refresh token)',
        request={'application/json': {'type': 'object', 'properties': {'refresh': {'type': 'string'}}}},
        responses={205: OpenApiResponse(description='Успешный выход')},
    )
    def post(self, request):
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response({'detail': 'Успешный выход из системы.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'detail': 'Неверный или просроченный токен.'}, status=status.HTTP_400_BAD_REQUEST)
