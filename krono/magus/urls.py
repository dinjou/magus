from django.urls import path
from . import views

app_name = 'magus'

urlpatterns = [
    path('csrf/', views.get_csrf_token, name='csrf'),
    path('register/', views.register, name='register'),
    path('clock_in/', views.clock_in, name='clock_in'),
    path('clock_out/', views.clock_out, name='clock_out'),
    path('tasks/', views.task_buttons, name='task_buttons'),
    path('', views.task_list, name='task_list'),
]