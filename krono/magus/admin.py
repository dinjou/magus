from django.contrib import admin
from .models import Profile, TaskType, Task, APIKey, ScheduledExport


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'timezone', 'theme', 'created_at']
    search_fields = ['user__username', 'user__email']
    list_filter = ['theme', 'enable_live_activities']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Settings', {
            'fields': ('email_for_exports', 'timezone', 'theme', 'long_press_duration', 'pinned_tasks_visible')
        }),
        ('Features', {
            'fields': ('enable_live_activities', 'openai_api_key_encrypted')
        }),
        ('Legacy Fields', {
            'fields': ('last_heartbeat', 'clock_in_time', 'clock_out_time', 'active_session'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'emoji', 'user', 'is_pinned', 'is_archived', 'sort_order']
    search_fields = ['name', 'user__username']
    list_filter = ['is_pinned', 'is_archived', 'user']
    ordering = ['user', 'sort_order', 'name']
    list_editable = ['sort_order', 'is_pinned']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_task_name', 'start_time', 'end_time', 'interrupted', 'get_duration']
    search_fields = ['user__username', 'task_type__name', 'notes']
    list_filter = ['interrupted', 'is_manual_entry', 'edited_by_user', 'task_type']
    readonly_fields = ['created_at', 'updated_at', 'get_duration']
    date_hierarchy = 'start_time'
    
    def get_task_name(self, obj):
        """Display task type with emoji"""
        return f"{obj.task_type.emoji} {obj.task_type.name}"
    get_task_name.short_description = 'Task Type'
    
    def get_duration(self, obj):
        """Display duration in human-readable format"""
        if obj.end_time:
            duration = obj.duration_timedelta
            hours = duration.total_seconds() // 3600
            minutes = (duration.total_seconds() % 3600) // 60
            return f"{int(hours)}h {int(minutes)}m"
        return "⏱️ Ongoing"
    get_duration.short_description = 'Duration'


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'key_prefix', 'is_active', 'created_at', 'last_used']
    search_fields = ['name', 'user__username', 'key_prefix']
    list_filter = ['is_active', 'can_read', 'can_write']
    readonly_fields = ['key_hash', 'key_prefix', 'created_at', 'last_used']
    
    def has_add_permission(self, request):
        """Prevent creating API keys through admin (should use API)"""
        return False


@admin.register(ScheduledExport)
class ScheduledExportAdmin(admin.ModelAdmin):
    list_display = ['user', 'frequency', 'email_to', 'is_active', 'last_sent', 'next_scheduled']
    search_fields = ['user__username', 'email_to']
    list_filter = ['frequency', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'last_sent']
    list_editable = ['is_active']
