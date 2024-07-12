from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task

TASK_TYPES = [
    "Outages", "Installs", "Tier 2 Assistance", "AE Escalations",
    "Emails/Messages", "CWRV", "VoIP", "NOC Tasks", "IT Support Tasks",
    "Meetings", "Meal Break", "Other", "Total"
]

@login_required
def task_buttons(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        task_type = request.POST.get('task_type')
        if action == 'start':
            existing_task = Task.objects.filter(user=request.user, end_time__isnull=True).first()
            if existing_task:
                existing_task.end_time = timezone.now()
                existing_task.interrupted = True
                existing_task.save()
            Task.objects.create(user=request.user, task_type=task_type, start_time=timezone.now())
        elif action == 'end':
            task = Task.objects.filter(user=request.user, task_type=task_type, end_time__isnull=True).first()
            if task:
                task.end_time = timezone.now()
                task.save()
        return redirect('magus:task_buttons')
    return render(request, 'magus/task_buttons.html', {'task_types': TASK_TYPES})

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'magus/task_list.html', {'tasks': tasks})
