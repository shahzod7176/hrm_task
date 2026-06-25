from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.utils import extend_schema

from api.views.auth_views import RegisterView, LogoutView
from api.views.employee_views import EmployeeViewSet
from api.views.task_views import TaskViewSet

# JWT viewlarni swagger uchun tag qilamiz
TokenObtainPairView = extend_schema(
    tags=['auth'], summary='Вход в систему — получить JWT токены'
)(TokenObtainPairView)

TokenRefreshView = extend_schema(
    tags=['auth'], summary='Обновить access токен через refresh'
)(TokenRefreshView)

TokenVerifyView = extend_schema(
    tags=['auth'], summary='Проверить валидность токена'
)(TokenVerifyView)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'tasks',     TaskViewSet,     basename='task')

urlpatterns = [
    # ── Auth ──────────────────────────────────────────────────────────────────
    path('auth/register/', RegisterView.as_view(),       name='register'),
    path('auth/login/',    TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/',  TokenRefreshView.as_view(),    name='token_refresh'),
    path('auth/verify/',   TokenVerifyView.as_view(),     name='token_verify'),
    path('auth/logout/',   LogoutView.as_view(),          name='logout'),

    # ── Resources ─────────────────────────────────────────────────────────────
    path('', include(router.urls)),
]
