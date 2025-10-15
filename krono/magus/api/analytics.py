from django.db.models import Sum, Count, Q, F
from django.db.models.functions import TruncDate, TruncHour
from django.utils import timezone
from datetime import timedelta, datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from magus.models import Task, TaskType


@extend_schema(
    tags=['analytics'],
    responses={200: OpenApiResponse(description='Today\'s summary by task type')},
    description='Get today\'s time tracking summary grouped by task type',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def summary_today(request):
    """
    Get today's summary of time tracked per task type.
    
    Returns total duration for each task type tracked today.
    """
    today = timezone.now().date()
    
    tasks = Task.objects.filter(
        user=request.user,
        start_time__date=today,
        end_time__isnull=False  # Only completed tasks
    ).select_related('task_type')
    
    # Group by task type and sum durations
    summary = []
    task_types = {}
    
    for task in tasks:
        type_id = task.task_type.id
        if type_id not in task_types:
            task_types[type_id] = {
                'task_type_id': type_id,
                'task_type_name': task.task_type.name,
                'task_type_emoji': task.task_type.emoji,
                'task_type_color': task.task_type.color,
                'total_duration': 0,
                'task_count': 0,
                'interrupted_count': 0,
            }
        
        duration = task.duration
        task_types[type_id]['total_duration'] += duration
        task_types[type_id]['task_count'] += 1
        if task.interrupted:
            task_types[type_id]['interrupted_count'] += 1
    
    summary = list(task_types.values())
    
    # Calculate total time tracked today
    total_tracked = sum(item['total_duration'] for item in summary)
    
    # Format durations
    for item in summary:
        hours = int(item['total_duration'] // 3600)
        minutes = int((item['total_duration'] % 3600) // 60)
        item['duration_formatted'] = f"{hours}h {minutes}m"
        item['percentage'] = (item['total_duration'] / total_tracked * 100) if total_tracked > 0 else 0
    
    # Sort by duration descending
    summary.sort(key=lambda x: x['total_duration'], reverse=True)
    
    return Response({
        'date': today.isoformat(),
        'total_tracked': total_tracked,
        'total_tracked_formatted': f"{int(total_tracked // 3600)}h {int((total_tracked % 3600) // 60)}m",
        'task_types': summary,
    })


@extend_schema(
    tags=['analytics'],
    parameters=[
        OpenApiParameter(name='date', type=str, description='Date in YYYY-MM-DD format'),
    ],
    responses={200: OpenApiResponse(description='Daily breakdown')},
    description='Get time tracking breakdown for a specific day',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def daily_breakdown(request):
    """Get daily breakdown for a specific date"""
    date_str = request.query_params.get('date')
    
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    else:
        target_date = timezone.now().date()
    
    # Reuse summary logic
    tasks = Task.objects.filter(
        user=request.user,
        start_time__date=target_date,
        end_time__isnull=False
    ).select_related('task_type')
    
    task_types = {}
    for task in tasks:
        type_id = task.task_type.id
        if type_id not in task_types:
            task_types[type_id] = {
                'task_type_id': type_id,
                'task_type_name': task.task_type.name,
                'task_type_emoji': task.task_type.emoji,
                'task_type_color': task.task_type.color,
                'total_duration': 0,
                'task_count': 0,
            }
        task_types[type_id]['total_duration'] += task.duration
        task_types[type_id]['task_count'] += 1
    
    summary = list(task_types.values())
    total_tracked = sum(item['total_duration'] for item in summary)
    
    for item in summary:
        hours = int(item['total_duration'] // 3600)
        minutes = int((item['total_duration'] % 3600) // 60)
        item['duration_formatted'] = f"{hours}h {minutes}m"
        item['percentage'] = (item['total_duration'] / total_tracked * 100) if total_tracked > 0 else 0
    
    summary.sort(key=lambda x: x['total_duration'], reverse=True)
    
    return Response({
        'date': target_date.isoformat(),
        'total_tracked': total_tracked,
        'total_tracked_formatted': f"{int(total_tracked // 3600)}h {int((total_tracked % 3600) // 60)}m",
        'task_types': summary,
    })


@extend_schema(
    tags=['analytics'],
    parameters=[
        OpenApiParameter(name='start_date', type=str, description='Start date YYYY-MM-DD'),
        OpenApiParameter(name='end_date', type=str, description='End date YYYY-MM-DD'),
    ],
    responses={200: OpenApiResponse(description='Weekly aggregates')},
    description='Get weekly time tracking aggregates',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_breakdown(request):
    """Get weekly breakdown (last 7 days by default)"""
    end_date_str = request.query_params.get('end_date')
    start_date_str = request.query_params.get('start_date')
    
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid end_date format'}, status=400)
    else:
        end_date = timezone.now().date()
    
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid start_date format'}, status=400)
    else:
        start_date = end_date - timedelta(days=6)  # Last 7 days
    
    # Get daily summaries
    daily_data = []
    current_date = start_date
    
    while current_date <= end_date:
        tasks = Task.objects.filter(
            user=request.user,
            start_time__date=current_date,
            end_time__isnull=False
        )
        
        total = sum(task.duration for task in tasks)
        daily_data.append({
            'date': current_date.isoformat(),
            'total_duration': total,
            'total_formatted': f"{int(total // 3600)}h {int((total % 3600) // 60)}m",
        })
        
        current_date += timedelta(days=1)
    
    # Overall summary by task type
    tasks = Task.objects.filter(
        user=request.user,
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        end_time__isnull=False
    ).select_related('task_type')
    
    task_types = {}
    for task in tasks:
        type_id = task.task_type.id
        if type_id not in task_types:
            task_types[type_id] = {
                'task_type_id': type_id,
                'task_type_name': task.task_type.name,
                'task_type_emoji': task.task_type.emoji,
                'task_type_color': task.task_type.color,
                'total_duration': 0,
            }
        task_types[type_id]['total_duration'] += task.duration
    
    summary = list(task_types.values())
    total_tracked = sum(item['total_duration'] for item in summary)
    
    for item in summary:
        hours = int(item['total_duration'] // 3600)
        minutes = int((item['total_duration'] % 3600) // 60)
        item['duration_formatted'] = f"{hours}h {minutes}m"
        item['percentage'] = (item['total_duration'] / total_tracked * 100) if total_tracked > 0 else 0
    
    summary.sort(key=lambda x: x['total_duration'], reverse=True)
    
    return Response({
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'daily_data': daily_data,
        'task_type_summary': summary,
        'total_tracked': total_tracked,
        'total_tracked_formatted': f"{int(total_tracked // 3600)}h {int((total_tracked % 3600) // 60)}m",
    })


@extend_schema(
    tags=['analytics'],
    parameters=[
        OpenApiParameter(name='start_date', type=str, description='Start date YYYY-MM-DD'),
        OpenApiParameter(name='end_date', type=str, description='End date YYYY-MM-DD'),
    ],
    responses={200: OpenApiResponse(description='Monthly aggregates')},
    description='Get monthly time tracking aggregates',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_breakdown(request):
    """Get monthly breakdown"""
    end_date_str = request.query_params.get('end_date')
    start_date_str = request.query_params.get('start_date')
    
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid end_date format'}, status=400)
    else:
        end_date = timezone.now().date()
    
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid start_date format'}, status=400)
    else:
        # First day of current month
        start_date = end_date.replace(day=1)
    
    tasks = Task.objects.filter(
        user=request.user,
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        end_time__isnull=False
    ).select_related('task_type')
    
    task_types = {}
    for task in tasks:
        type_id = task.task_type.id
        if type_id not in task_types:
            task_types[type_id] = {
                'task_type_id': type_id,
                'task_type_name': task.task_type.name,
                'task_type_emoji': task.task_type.emoji,
                'task_type_color': task.task_type.color,
                'total_duration': 0,
                'task_count': 0,
            }
        task_types[type_id]['total_duration'] += task.duration
        task_types[type_id]['task_count'] += 1
    
    summary = list(task_types.values())
    total_tracked = sum(item['total_duration'] for item in summary)
    
    for item in summary:
        hours = int(item['total_duration'] // 3600)
        minutes = int((item['total_duration'] % 3600) // 60)
        item['duration_formatted'] = f"{hours}h {minutes}m"
        item['percentage'] = (item['total_duration'] / total_tracked * 100) if total_tracked > 0 else 0
    
    summary.sort(key=lambda x: x['total_duration'], reverse=True)
    
    return Response({
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'task_type_summary': summary,
        'total_tracked': total_tracked,
        'total_tracked_formatted': f"{int(total_tracked // 3600)}h {int((total_tracked % 3600) // 60)}m",
    })


@extend_schema(
    tags=['analytics'],
    parameters=[
        OpenApiParameter(name='start_date', type=str, description='Start date YYYY-MM-DD'),
        OpenApiParameter(name='end_date', type=str, description='End date YYYY-MM-DD'),
    ],
    responses={200: OpenApiResponse(description='Heatmap data')},
    description='Get activity heatmap data for calendar visualization',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def heatmap_data(request):
    """
    Get heatmap data showing activity levels per day.
    
    Returns total hours tracked per day for heatmap visualization.
    """
    end_date_str = request.query_params.get('end_date')
    start_date_str = request.query_params.get('start_date')
    
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = timezone.now().date()
    
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = end_date - timedelta(days=89)  # ~3 months
    
    # Get all tasks in date range
    tasks = Task.objects.filter(
        user=request.user,
        start_time__date__gte=start_date,
        start_time__date__lte=end_date,
        end_time__isnull=False
    ).annotate(
        date=TruncDate('start_time')
    ).values('date').annotate(
        total_duration=Sum(F('end_time') - F('start_time'))
    )
    
    # Convert to dict for easy lookup
    heatmap = []
    for item in tasks:
        total_seconds = item['total_duration'].total_seconds()
        hours = total_seconds / 3600
        heatmap.append({
            'date': item['date'].isoformat(),
            'hours': round(hours, 2),
            'level': min(4, int(hours // 2)),  # 0-4 intensity levels
        })
    
    return Response({
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'heatmap': heatmap,
    })

