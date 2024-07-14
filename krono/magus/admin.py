from django.contrib import admin

from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "task_type",
        "start_time",
        "end_time",
        "interrupted",
    ]
    list_per_page = 25
    readonly_fields = [
        "user",
        "task_type",
    ]
