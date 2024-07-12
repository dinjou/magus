from django.urls import path
from . import views

app_name = 'magus'

urlpatterns = [
    path('tasks/', views.task_buttons, name='task_buttons'),
    path('', views.task_list, name='task_list'),
]
