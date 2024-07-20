import json

from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.template.base import logger
from django.views.decorators.csrf import csrf_exempt

from .forms import UserRegisterForm
from .models import Task, Profile
from django.utils import timezone
from django.contrib import messages

TASK_TYPES = [
    "Outages", "Installs", "Tier 2 Assistance", "AE Escalations",
    "Emails/Messages", "CWRV", "VoIP", "NOC Tasks","Technician Phone Call", "Meetings",
    "Meal Break", "Non-Meal Break", "IT Support", "Other"
]


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('magus:task_buttons')
    else:
        form = UserRegisterForm()
    return render(request, 'magus/register.html', {'form': form})


def clock_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                user.profile.clock_in_time = timezone.now()
                user.profile.active_session = True
                user.profile.save()
                return redirect('magus:task_buttons')
    else:
        form = AuthenticationForm()
    return render(request, 'magus/clock_in.html', {'form': form})


@login_required
def clock_out(request):
    user = request.user
    # Check for active tasks
    active_tasks = Task.objects.filter(user=user, end_time__isnull=True)
    if active_tasks.exists():
        # Prevent clock out and notify the user
        messages.error(request, 'You have active tasks that need to be ended before clocking out.')
        return redirect('magus:task_buttons')

    if request.method == 'POST':
        user.profile.active_session = False
        user.profile.save()
        logout(request)
        return redirect('magus:clock_in')
    return render(request, 'magus/clock_out.html')



@login_required
def task_buttons(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        task_type = request.POST.get('task_type')

        if action == 'start':
            # Check if there is an ongoing task
            existing_task = Task.objects.filter(user=request.user, end_time__isnull=True).first()
            if existing_task:
                existing_task.end_time = timezone.now()
                existing_task.interrupted = True
                existing_task.save()
                messages.warning(request, f"Interrupted {existing_task.task_type} task and started {task_type} task.")
            else:
                messages.success(request, f"Started {task_type} task.")
            Task.objects.create(user=request.user, task_type=task_type, start_time=timezone.now())
            return redirect('magus:task_buttons')

        elif action == 'end':
            task = Task.objects.filter(user=request.user, task_type=task_type, end_time__isnull=True).first()
            if task:
                task.end_time = timezone.now()
                task.save()
                messages.success(request, f"Ended {task_type} task.")
            else:
                messages.error(request, f"No active {task_type} task to end.")
            return redirect('magus:task_buttons')

    recent_task = Task.objects.filter(user=request.user).order_by('-start_time').first()

    return render(request, 'magus/task_buttons.html', {
        'task_types': TASK_TYPES,
        'user': request.user,
        'recent_task': recent_task,
        'is_ongoing': recent_task.end_time is None if recent_task else False
    })


@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'magus/task_list.html', {'tasks': tasks})

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@login_required
@csrf_exempt
def heartbeat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('status') == 'alive':
            request.user.profile.last_heartbeat = timezone.now()
            request.user.profile.save()
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

