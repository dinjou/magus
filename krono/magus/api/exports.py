import csv
import io
from datetime import datetime
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from magus.models import Task, ScheduledExport
from magus.tasks import send_csv_export_email


@extend_schema(
    tags=['export'],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'start_date': {'type': 'string', 'description': 'YYYY-MM-DD'},
                'end_date': {'type': 'string', 'description': 'YYYY-MM-DD'},
                'email_to': {'type': 'string', 'format': 'email'},
            },
            'required': ['email_to']
        }
    },
    responses={
        200: OpenApiResponse(description='CSV export queued successfully'),
        400: OpenApiResponse(description='Invalid request'),
    },
    description='Generate CSV export and send via email',
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def export_csv(request):
    """
    Generate CSV export of time tracking data and email it.
    
    Queues a Celery task to generate and send the export asynchronously.
    """
    start_date_str = request.data.get('start_date')
    end_date_str = request.data.get('end_date')
    email_to = request.data.get('email_to')
    
    if not email_to:
        return Response(
            {'error': 'email_to is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Parse dates
    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = timezone.now().date() - timezone.timedelta(days=30)
        
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = timezone.now().date()
    except ValueError:
        return Response(
            {'error': 'Invalid date format. Use YYYY-MM-DD'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Queue export task
    send_csv_export_email.delay(
        request.user.id,
        start_date.isoformat(),
        end_date.isoformat(),
        email_to
    )
    
    return Response({
        'message': f'CSV export queued. You will receive it at {email_to} shortly.',
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
    })


@extend_schema(
    tags=['export'],
    responses={200: OpenApiResponse(description='Download CSV file')},
    parameters=[
        OpenApiParameter(name='start_date', type=str, description='YYYY-MM-DD'),
        OpenApiParameter(name='end_date', type=str, description='YYYY-MM-DD'),
    ],
    description='Download CSV export directly (no email)',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_csv(request):
    """
    Generate and download CSV export directly.
    
    Useful for immediate downloads without email.
    """
    from django.http import HttpResponse
    
    start_date_str = request.query_params.get('start_date')
    end_date_str = request.query_params.get('end_date')
    
    # Parse dates
    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = timezone.now().date() - timezone.timedelta(days=30)
        
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = timezone.now().date()
    except ValueError:
        return Response(
            {'error': 'Invalid date format. Use YYYY-MM-DD'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get tasks
    tasks = Task.objects.filter(
        user=request.user,
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
        
        # Convert to user timezone (would use profile timezone in production)
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
    
    # Create response
    response = HttpResponse(output.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="magus_export_{start_date}_{end_date}.csv"'
    
    return response

