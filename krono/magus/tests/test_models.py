"""
Basic model tests for MAGUS
"""
import pytest
from django.contrib.auth.models import User
from magus.models import Profile, TaskType, Task, APIKey


@pytest.mark.django_db
class TestModels:
    """Test database models"""
    
    def test_user_profile_created_on_signup(self):
        """Test that profile is auto-created when user is created"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        assert hasattr(user, 'profile')
        assert user.profile is not None
    
    def test_default_task_types_created(self):
        """Test that default task types are created for new users"""
        user = User.objects.create_user(username='testuser2', password='testpass123')
        task_types = TaskType.objects.filter(user=user)
        assert task_types.count() == 7  # Default task types
    
    def test_task_duration_calculation(self):
        """Test task duration property"""
        from django.utils import timezone
        from datetime import timedelta
        
        user = User.objects.create_user(username='testuser3', password='testpass123')
        task_type = TaskType.objects.filter(user=user).first()
        
        start = timezone.now()
        end = start + timedelta(hours=1, minutes=30)
        
        task = Task.objects.create(
            user=user,
            task_type=task_type,
            start_time=start,
            end_time=end
        )
        
        # Duration should be ~5400 seconds (1.5 hours)
        assert 5395 < task.duration < 5405
    
    def test_api_key_generation(self):
        """Test API key generation and hashing"""
        key = APIKey.generate_key()
        assert key.startswith('magus_')
        assert len(key) > 20
        
        key_hash = APIKey.hash_key(key)
        assert len(key_hash) == 64  # SHA-256 hex

