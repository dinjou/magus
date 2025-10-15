import hashlib
import secrets
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import EmailValidator


class Profile(models.Model):
    """Extended user profile with app settings and preferences"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Email settings
    email_for_exports = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        help_text="Email address for receiving CSV exports"
    )
    
    # User preferences
    timezone = models.CharField(max_length=50, default='America/Denver')
    theme = models.CharField(
        max_length=20,
        default='dark',
        choices=[
            ('dark', 'Dark'),
            ('light', 'Light'),
            ('aqua', 'Aqua (Mac OS X)'),
            ('aero', 'Aero (Windows 7)'),
            ('metro', 'Metro (Windows 8)'),
            ('luna', 'Luna (Windows XP)'),
        ]
    )
    long_press_duration = models.FloatField(
        default=1.5,
        help_text="Duration in seconds for long-press gesture"
    )
    pinned_tasks_visible = models.IntegerField(
        default=4,
        help_text="Number of pinned tasks to show in quick grid"
    )
    
    # Features
    enable_live_activities = models.BooleanField(default=True)
    openai_api_key_encrypted = models.CharField(
        max_length=255,
        blank=True,
        help_text="Encrypted OpenAI API key for AI insights"
    )
    
    # Legacy fields (will be removed after migration)
    last_heartbeat = models.DateTimeField(null=True, blank=True)
    clock_in_time = models.DateTimeField(null=True, blank=True)
    clock_out_time = models.DateTimeField(null=True, blank=True)
    active_session = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Profile: {self.user.username}"


class TaskType(models.Model):
    """User-customizable task categories"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_types')
    name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10, default='📊')
    color = models.CharField(max_length=7, default='#3A8E61', help_text="Hex color code")
    
    # Organization
    is_pinned = models.BooleanField(default=False, help_text="Show in quick start grid")
    is_archived = models.BooleanField(default=False, help_text="Soft delete - hidden from UI")
    sort_order = models.IntegerField(default=0, help_text="Display order (lower = first)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']
        unique_together = ['user', 'name']
        indexes = [
            models.Index(fields=['user', 'is_archived']),
            models.Index(fields=['user', 'is_pinned']),
        ]

    def __str__(self):
        return f"{self.emoji} {self.name} ({self.user.username})"


class Task(models.Model):
    """Time tracking entries"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.PROTECT,
        related_name='tasks',
        help_text="Task type cannot be deleted if tasks reference it"
    )
    
    # Timestamps (stored in UTC)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    
    # Status
    interrupted = models.BooleanField(
        default=False,
        help_text="True if task was stopped by starting another task"
    )
    is_manual_entry = models.BooleanField(
        default=False,
        help_text="True if created/edited manually vs tracked live"
    )
    
    # Optional metadata
    notes = models.TextField(blank=True)
    
    # Audit trail
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited_by_user = models.BooleanField(
        default=False,
        help_text="True if user manually edited this entry"
    )

    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['user', '-start_time']),
            models.Index(fields=['user', 'end_time']),
            models.Index(fields=['user', 'task_type', '-start_time']),
        ]

    def __str__(self):
        status = "ongoing" if not self.end_time else "completed"
        return f"{self.user.username} - {self.task_type.name} ({status})"

    @property
    def duration(self):
        """Calculate duration in seconds"""
        if not self.end_time:
            # Ongoing task - duration from start until now
            return (timezone.now() - self.start_time).total_seconds()
        return (self.end_time - self.start_time).total_seconds()
    
    @property
    def duration_timedelta(self):
        """Get duration as timedelta object"""
        if not self.end_time:
            return timezone.now() - self.start_time
        return self.end_time - self.start_time


class APIKey(models.Model):
    """User-generated API keys for automation"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(
        max_length=100,
        help_text="Descriptive name (e.g., 'Home Automation', 'iOS Shortcuts')"
    )
    key_prefix = models.CharField(
        max_length=8,
        help_text="First 8 characters of key for display"
    )
    key_hash = models.CharField(
        max_length=128,
        unique=True,
        help_text="SHA-256 hash of the API key"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Permissions (for future granular access control)
    can_read = models.BooleanField(default=True)
    can_write = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.key_prefix}...)"

    @staticmethod
    def generate_key():
        """Generate a secure random API key"""
        return f"magus_{secrets.token_urlsafe(32)}"

    @staticmethod
    def hash_key(key: str):
        """Hash an API key using SHA-256"""
        return hashlib.sha256(key.encode()).hexdigest()

    def verify_key(self, key: str):
        """Verify a provided key matches this API key"""
        return self.key_hash == self.hash_key(key)


class ScheduledExport(models.Model):
    """Automated CSV export scheduling"""
    
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scheduled_exports')
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    email_to = models.EmailField(validators=[EmailValidator()])
    is_active = models.BooleanField(default=True)
    
    # Schedule tracking
    last_sent = models.DateTimeField(null=True, blank=True)
    next_scheduled = models.DateTimeField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['next_scheduled']

    def __str__(self):
        return f"{self.user.username} - {self.get_frequency_display()} export to {self.email_to}"

    def calculate_next_scheduled(self):
        """Calculate next scheduled export time based on frequency"""
        now = timezone.now()
        if self.frequency == 'daily':
            return now + timedelta(days=1)
        elif self.frequency == 'weekly':
            return now + timedelta(weeks=1)
        elif self.frequency == 'monthly':
            # Approximate 30 days
            return now + timedelta(days=30)
        return now

    def save(self, *args, **kwargs):
        """Auto-calculate next_scheduled if not set"""
        if not self.next_scheduled:
            self.next_scheduled = self.calculate_next_scheduled()
        super().save(*args, **kwargs)
