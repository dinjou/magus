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
    logger.info(f"User {username} missed a heartbeat.")
    try:
        user = User.objects.get(id=user_id)
        # End the current task or mark as interrupted
        ongoing_task = Task.objects.filter(user=user, end_time__isnull=True).first()
        if ongoing_task:
            ongoing_task.end_time = timezone.now()
            ongoing_task.interrupted = True
            ongoing_task.save()
        # Set monitor_heartbeat to False, prevent further checks until user logs in again
        user.profile.active_session = False
        user.profile.save()
        logger.info(f"Set active_session to False for user {username}")
    except User.DoesNotExist:
        logger.warning(f"User with id {user_id} does not exist")
