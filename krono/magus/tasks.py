from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Task
import logging

logger = logging.getLogger('magus')

@shared_task
def check_heartbeats():
    threshold = timezone.now() - timezone.timedelta(seconds=60)
    users = User.objects.filter(profile__last_heartbeat__lt=threshold)
    for user in users:
        handle_missed_heartbeat.delay(user.id, user.username)

@shared_task
def handle_missed_heartbeat(user_id, username):
    print(f"User {username} missed a heartbeat.")
    # End the current task or mark as interrupted
    ongoing_task = Task.objects.filter(user=user_id, end_time__isnull=True).first()
    if ongoing_task:
        ongoing_task.end_time = timezone.now()
        ongoing_task.interrupted = True
        ongoing_task.save()
