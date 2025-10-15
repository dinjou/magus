"""
API endpoint tests for MAGUS
"""
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from magus.models import TaskType


@pytest.mark.django_db
class TestAuthAPI:
    """Test authentication endpoints"""
    
    def test_user_registration(self):
        """Test user can register via API"""
        client = APIClient()
        response = client.post('/api/auth/register/', {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'testpass123',
            'password2': 'testpass123',
        })
        assert response.status_code == 201
        assert 'tokens' in response.data
        assert User.objects.filter(username='newuser').exists()
    
    def test_user_login(self):
        """Test user can login and receive JWT token"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        
        client = APIClient()
        response = client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123',
        })
        
        assert response.status_code == 200
        assert 'tokens' in response.data
        assert 'access' in response.data['tokens']


@pytest.mark.django_db
class TestTaskTypeAPI:
    """Test task type endpoints"""
    
    def test_list_task_types(self):
        """Test authenticated user can list their task types"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.get('/api/task-types/')
        assert response.status_code == 200
        assert len(response.data['results']) == 7  # Default task types
    
    def test_create_task_type(self):
        """Test user can create custom task type"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.post('/api/task-types/', {
            'name': 'Custom Task',
            'emoji': '🚀',
            'color': '#FF0000',
        })
        
        assert response.status_code == 201
        assert response.data['name'] == 'Custom Task'


@pytest.mark.django_db
class TestTaskTrackingAPI:
    """Test time tracking endpoints"""
    
    def test_start_task(self):
        """Test starting a task"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        task_type = TaskType.objects.filter(user=user).first()
        
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.post('/api/tasks/start/', {
            'task_type_id': task_type.id
        })
        
        assert response.status_code == 201
        assert response.data['task_type_detail']['name'] == task_type.name
        assert response.data['end_time'] is None
    
    def test_stop_task(self):
        """Test stopping a task"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        task_type = TaskType.objects.filter(user=user).first()
        
        client = APIClient()
        client.force_authenticate(user=user)
        
        # Start task
        client.post('/api/tasks/start/', {'task_type_id': task_type.id})
        
        # Stop task
        response = client.post('/api/tasks/stop/')
        
        assert response.status_code == 200
        assert response.data['end_time'] is not None

