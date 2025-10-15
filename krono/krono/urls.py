"""
URL configuration for krono project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


def health_check(request):
    """Simple health check endpoint for Docker health checks"""
    return JsonResponse({'status': 'healthy'})


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health check
    path('health/', health_check, name='health'),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API endpoints (will be created in Sprint 1+)
    # path('api/', include('magus.api.urls')),
    
    # Legacy magus URLs (will be deprecated after migration)
    path('magus/', include('magus.urls')),
]
