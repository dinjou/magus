from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm
from .models import Task, Profile
from django.utils import timezone
from django.contrib import messages


TASK_TYPES = [
    "Outages", "Installs", "Tier 2 Assistance", "AE Escalations",
    "Emails/Messages", "CWRV", "VoIP", "NOC Tasks", "Meetings",
    "Meal Break", "Other", "Total"
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
                user.profile.save()
                return redirect('magus:task_buttons')
    else:
        form = AuthenticationForm()
    return render(request, 'magus/clock_in.html', {'form': form})

@login_required
def clock_out(request):
    user = request.user
    user.profile.clock_out_time = timezone.now()
    user.profile.save()
    logout(request)
    return redirect('magus:clock_in')


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
            messages.success(request, f"Started {task_type} task.")

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

