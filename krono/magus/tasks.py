import csv
import io
from datetime import datetime
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils import timezone
from .models import Task
import logging

logger = logging.getLogger('magus')


@shared_task
def check_heartbeats():
    """Legacy heartbeat check - kept for compatibility"""
    threshold = timezone.now() - timezone.timedelta(seconds=60)
    users = User.objects.filter(profile__last_heartbeat__lt=threshold)
    for user in users:
        handle_missed_heartbeat.delay(user.id, user.username)


@shared_task
def handle_missed_heartbeat(user_id, username):
    """Legacy heartbeat handler - kept for compatibility"""
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


@shared_task
def send_csv_export_email(user_id, start_date_str, end_date_str, email_to):
    """
    Generate CSV export and send via email.
    
    Args:
        user_id: User ID
        start_date_str: Start date in ISO format (YYYY-MM-DD)
        end_date_str: End date in ISO format (YYYY-MM-DD)
        email_to: Email address to send to
    """
    try:
        user = User.objects.get(id=user_id)
        start_date = datetime.fromisoformat(start_date_str).date()
        end_date = datetime.fromisoformat(end_date_str).date()
        
        # Get tasks
        tasks = Task.objects.filter(
            user=user,
            start_time__date__gte=start_date,
            start_time__date__lte=end_date,
            end_time__isnull=False
        ).select_related('task_type').order_by('start_time')
        
        # Generate CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            'Date',
            'Task Type',
            'Start Time',
            'End Time',
            'Duration (HH:MM:SS)',
            'Interrupted',
            'Notes',
            'Edited'
        ])
        
        # Rows
        for task in tasks:
            duration_seconds = task.duration
            hours = int(duration_seconds // 3600)
            minutes = int((duration_seconds % 3600) // 60)
            seconds = int(duration_seconds % 60)
            duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            # Convert to user timezone
            start_local = timezone.localtime(task.start_time)
            end_local = timezone.localtime(task.end_time) if task.end_time else None
            
            writer.writerow([
                start_local.strftime('%Y-%m-%d'),
                task.task_type.name,
                start_local.strftime('%Y-%m-%d %H:%M:%S'),
                end_local.strftime('%Y-%m-%d %H:%M:%S') if end_local else '',
                duration_str,
                'Yes' if task.interrupted else 'No',
                task.notes,
                'Yes' if task.edited_by_user else 'No',
            ])
        
        # Create email
        subject = f'MAGUS Time Tracking Export - {start_date} to {end_date}'
        body = f"""Hi {user.username},

Your time tracking data export is attached.

Export Details:
- Date Range: {start_date} to {end_date}
- Total Entries: {tasks.count()}
- Generated: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

This export was generated from your MAGUS instance.
"""
        
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email='noreply@magus.local',
            to=[email_to],
        )
        
        # Attach CSV
        email.attach(
            f'magus_export_{start_date}_{end_date}.csv',
            output.getvalue(),
            'text/csv'
        )
        
        email.send()
        
        logger.info(f"CSV export sent to {email_to} for user {user.username}")
        
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist")
    except Exception as e:
        logger.error(f"Error generating CSV export: {str(e)}")
        raise
