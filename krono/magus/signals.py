from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, TaskType


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create Profile and default TaskTypes for new users"""
    if created:
        # Create profile
        Profile.objects.create(user=instance)
        
        # Create default task types
        default_tasks = [
            {'name': 'Deep Work', 'emoji': '💻', 'color': '#3A8E61', 'is_pinned': True, 'sort_order': 0},
            {'name': 'Email', 'emoji': '📧', 'color': '#7289DA', 'is_pinned': True, 'sort_order': 1},
            {'name': 'Meeting', 'emoji': '🤝', 'color': '#8B7D5A', 'is_pinned': True, 'sort_order': 2},
            {'name': 'Break', 'emoji': '🍔', 'color': '#B35A5A', 'is_pinned': True, 'sort_order': 3},
            {'name': 'Call', 'emoji': '📞', 'color': '#9B59B6', 'is_pinned': False, 'sort_order': 4},
            {'name': 'Admin', 'emoji': '📋', 'color': '#95A5A6', 'is_pinned': False, 'sort_order': 5},
            {'name': 'Other', 'emoji': '📊', 'color': '#7F8C8D', 'is_pinned': False, 'sort_order': 6},
        ]
        
        for task_data in default_tasks:
            TaskType.objects.create(user=instance, **task_data)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Ensure profile exists and is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
