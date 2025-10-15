from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views, analytics, exports
from .viewsets import TaskTypeViewSet, TaskViewSet
from .scheduled_exports import ScheduledExportViewSet
from .api_keys import APIKeyViewSet

app_name = 'api'

# Create router and register viewsets
router = DefaultRouter()
router.register(r'task-types', TaskTypeViewSet, basename='tasktype')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'scheduled-exports', ScheduledExportViewSet, basename='scheduledexport')
router.register(r'api-keys', APIKeyViewSet, basename='apikey')

urlpatterns = [
    # Authentication
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', views.current_user_view, name='current_user'),
    
    # Profile
    path('profile/', views.profile_detail_view, name='profile_detail'),
    path('profile/update/', views.profile_update_view, name='profile_update'),
    path('profile/delete/', views.profile_delete_view, name='profile_delete'),
    
    # Analytics
    path('analytics/summary/', analytics.summary_today, name='analytics_summary'),
    path('analytics/daily/', analytics.daily_breakdown, name='analytics_daily'),
    path('analytics/weekly/', analytics.weekly_breakdown, name='analytics_weekly'),
    path('analytics/monthly/', analytics.monthly_breakdown, name='analytics_monthly'),
    path('analytics/heatmap/', analytics.heatmap_data, name='analytics_heatmap'),
    
    # Export
    path('export/csv/', exports.export_csv, name='export_csv'),
    path('export/download/', exports.download_csv, name='export_download'),
    
    # ViewSet routes (task-types, tasks, scheduled-exports)
    path('', include(router.urls)),
]

