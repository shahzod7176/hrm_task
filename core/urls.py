from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── OpenAPI schema ─────────────────────────────────────────────────────────
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # ── Swagger UI  →  /swagger/ ───────────────────────────────────────────────
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ── ReDoc       →  /redoc/ ─────────────────────────────────────────────────
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # ── API routes ─────────────────────────────────────────────────────────────
    path('api/', include('api.urls')),
]
