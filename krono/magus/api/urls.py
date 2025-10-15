from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'api'

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
]

