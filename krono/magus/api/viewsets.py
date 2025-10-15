from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter

from magus.models import TaskType, Task
from .serializers import TaskTypeSerializer, TaskSerializer


@extend_schema_view(
    list=extend_schema(
        tags=['task-types'],
        description='List all task types for the current user. Excludes archived by default.',
        parameters=[
            OpenApiParameter(
                name='show_archived',
                type=bool,
                description='Include archived task types',
                required=False
            ),
            OpenApiParameter(
                name='is_pinned',
                type=bool,
                description='Filter by pinned status',
                required=False
            ),
        ]
    ),
    create=extend_schema(
        tags=['task-types'],
        description='Create a new task type',
    ),
    retrieve=extend_schema(
        tags=['task-types'],
        description='Get a specific task type',
    ),
    update=extend_schema(
        tags=['task-types'],
        description='Update a task type',
    ),
    partial_update=extend_schema(
        tags=['task-types'],
        description='Partially update a task type',
    ),
    destroy=extend_schema(
        tags=['task-types'],
        description='Archive a task type (soft delete)',
    ),
)
class TaskTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing task types.
    
    Provides CRUD operations plus custom actions for pinning and reordering.
    """
    serializer_class = TaskTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_pinned', 'is_archived']
    search_fields = ['name']
    ordering_fields = ['sort_order', 'name', 'created_at']
    ordering = ['sort_order', 'name']
    
    def get_queryset(self):
        """Filter task types by current user and optionally show archived"""
        queryset = TaskType.objects.filter(user=self.request.user)
        
        # Exclude archived by default
        show_archived = self.request.query_params.get('show_archived', 'false').lower() == 'true'
        if not show_archived:
            queryset = queryset.filter(is_archived=False)
        
        return queryset
    
    def perform_create(self, serializer):
        """Automatically set the user when creating a task type"""
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """
        Soft delete: Mark task type as archived instead of deleting.
        Prevents deletion if tasks reference this type (PROTECT foreign key).
        """
        instance = self.get_object()
        instance.is_archived = True
        instance.save()
        return Response(
            {'message': f'Task type "{instance.name}" archived successfully'},
            status=status.HTTP_200_OK
        )
    
    @extend_schema(
        tags=['task-types'],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'task_type_ids': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': 'Ordered list of task type IDs'
                    }
                },
                'required': ['task_type_ids']
            }
        },
        responses={
            200: OpenApiResponse(description='Task types reordered successfully'),
            400: OpenApiResponse(description='Invalid data'),
        },
        description='Reorder task types by providing an ordered list of IDs',
    )
    @action(detail=False, methods=['post'])
    def reorder(self, request):
        """
        Bulk reorder task types.
        
        Expects: {"task_type_ids": [3, 1, 5, 2, 4]}
        Sets sort_order based on position in array.
        """
        task_type_ids = request.data.get('task_type_ids', [])
        
        if not task_type_ids:
            return Response(
                {'error': 'task_type_ids is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify all IDs belong to current user
        user_task_types = self.get_queryset().filter(id__in=task_type_ids)
        
        if user_task_types.count() != len(task_type_ids):
            return Response(
                {'error': 'Invalid task type IDs or access denied'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update sort_order for each task type
        for index, task_type_id in enumerate(task_type_ids):
            TaskType.objects.filter(id=task_type_id).update(sort_order=index)
        
        return Response({'message': 'Task types reordered successfully'})
    
    @extend_schema(
        tags=['task-types'],
        responses={
            200: OpenApiResponse(
                description='Pin status toggled',
                response=TaskTypeSerializer
            ),
        },
        description='Toggle the pinned status of a task type',
    )
    @action(detail=True, methods=['post'])
    def toggle_pin(self, request, pk=None):
        """Toggle the is_pinned status of a task type"""
        task_type = self.get_object()
        task_type.is_pinned = not task_type.is_pinned
        task_type.save()
        
        serializer = self.get_serializer(task_type)
        return Response(serializer.data)
    
    @extend_schema(
        tags=['task-types'],
        responses={
            200: OpenApiResponse(
                description='Task type un-archived',
                response=TaskTypeSerializer
            ),
        },
        description='Un-archive a task type',
    )
    @action(detail=True, methods=['post'])
    def unarchive(self, request, pk=None):
        """Un-archive a task type"""
        task_type = self.get_object()
        task_type.is_archived = False
        task_type.save()
        
        serializer = self.get_serializer(task_type)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        tags=['tasks'],
        description='List all tasks for the current user',
        parameters=[
            OpenApiParameter(
                name='start_date',
                type=str,
                description='Filter tasks starting from this date (YYYY-MM-DD)',
                required=False
            ),
            OpenApiParameter(
                name='end_date',
                type=str,
                description='Filter tasks up to this date (YYYY-MM-DD)',
                required=False
            ),
            OpenApiParameter(
                name='task_type',
                type=int,
                description='Filter by task type ID',
                required=False
            ),
            OpenApiParameter(
                name='interrupted',
                type=bool,
                description='Filter by interrupted status',
                required=False
            ),
        ]
    ),
    create=extend_schema(
        tags=['tasks'],
        description='Create a new task entry (manual entry)',
    ),
    retrieve=extend_schema(
        tags=['tasks'],
        description='Get a specific task',
    ),
    update=extend_schema(
        tags=['tasks'],
        description='Update a task entry',
    ),
    partial_update=extend_schema(
        tags=['tasks'],
        description='Partially update a task entry',
    ),
    destroy=extend_schema(
        tags=['tasks'],
        description='Delete a task entry',
    ),
)
class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing time tracking tasks.
    
    Provides CRUD operations plus custom actions for starting/stopping tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['task_type', 'interrupted', 'is_manual_entry']
    ordering_fields = ['start_time', 'end_time', 'created_at']
    ordering = ['-start_time']
    
    def get_queryset(self):
        """Filter tasks by current user and optional date range"""
        queryset = Task.objects.filter(user=self.request.user)
        
        # Date filtering
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(start_time__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(start_time__date__lte=end_date)
        
        return queryset
    
    def perform_create(self, serializer):
        """Automatically set user and mark as manual entry"""
        serializer.save(
            user=self.request.user,
            is_manual_entry=True
        )
    
    def perform_update(self, serializer):
        """Mark task as edited when updated"""
        serializer.save(edited_by_user=True)
    
    @extend_schema(
        tags=['tasks'],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'task_type_id': {'type': 'integer'},
                    'notes': {'type': 'string'},
                },
                'required': ['task_type_id']
            }
        },
        responses={
            201: OpenApiResponse(
                description='Task started successfully',
                response=TaskSerializer
            ),
            400: OpenApiResponse(description='Already tracking a task'),
        },
        description='Start tracking a new task',
    )
    @action(detail=False, methods=['post'])
    def start(self, request):
        """
        Start tracking a new task.
        
        Returns 400 if user is already tracking a task.
        Use 'interrupt' action instead to stop current and start new.
        """
        from django.utils import timezone
        
        # Check if already tracking
        current_task = Task.objects.filter(
            user=request.user,
            end_time__isnull=True
        ).first()
        
        if current_task:
            return Response(
                {
                    'error': 'Already tracking a task',
                    'current_task_id': current_task.id,
                    'current_task_type': current_task.task_type.name,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task_type_id = request.data.get('task_type_id')
        notes = request.data.get('notes', '')
        
        if not task_type_id:
            return Response(
                {'error': 'task_type_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify task type belongs to user
        try:
            task_type = TaskType.objects.get(
                id=task_type_id,
                user=request.user,
                is_archived=False
            )
        except TaskType.DoesNotExist:
            return Response(
                {'error': 'Invalid task type ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create new task
        task = Task.objects.create(
            user=request.user,
            task_type=task_type,
            start_time=timezone.now(),
            notes=notes
        )
        
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        tags=['tasks'],
        responses={
            200: OpenApiResponse(
                description='Task stopped successfully',
                response=TaskSerializer
            ),
            400: OpenApiResponse(description='No active task to stop'),
        },
        description='Stop the currently tracking task',
    )
    @action(detail=False, methods=['post'])
    def stop(self, request):
        """
        Stop the currently tracking task.
        
        Returns 400 if no task is currently being tracked.
        """
        from django.utils import timezone
        
        current_task = Task.objects.filter(
            user=request.user,
            end_time__isnull=True
        ).first()
        
        if not current_task:
            return Response(
                {'error': 'No active task to stop'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        current_task.end_time = timezone.now()
        current_task.save()
        
        serializer = self.get_serializer(current_task)
        return Response(serializer.data)
    
    @extend_schema(
        tags=['tasks'],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'task_type_id': {'type': 'integer'},
                    'notes': {'type': 'string'},
                },
                'required': ['task_type_id']
            }
        },
        responses={
            200: OpenApiResponse(
                description='Task interrupted and new task started',
                response={
                    'type': 'object',
                    'properties': {
                        'interrupted_task': {'type': 'object'},
                        'new_task': {'type': 'object'},
                    }
                }
            ),
            400: OpenApiResponse(description='Invalid request'),
        },
        description='Stop current task (mark as interrupted) and start a new one atomically',
    )
    @action(detail=False, methods=['post'])
    def interrupt(self, request):
        """
        Atomically stop current task (mark as interrupted) and start new task.
        
        This is the preferred way to switch tasks without manually stopping first.
        """
        from django.utils import timezone
        from django.db import transaction
        
        task_type_id = request.data.get('task_type_id')
        notes = request.data.get('notes', '')
        
        if not task_type_id:
            return Response(
                {'error': 'task_type_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify task type belongs to user
        try:
            task_type = TaskType.objects.get(
                id=task_type_id,
                user=request.user,
                is_archived=False
            )
        except TaskType.DoesNotExist:
            return Response(
                {'error': 'Invalid task type ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            # Stop current task if exists
            current_task = Task.objects.filter(
                user=request.user,
                end_time__isnull=True
            ).first()
            
            interrupted_task_data = None
            if current_task:
                current_task.end_time = timezone.now()
                current_task.interrupted = True
                current_task.save()
                interrupted_task_data = self.get_serializer(current_task).data
            
            # Start new task
            new_task = Task.objects.create(
                user=request.user,
                task_type=task_type,
                start_time=timezone.now(),
                notes=notes
            )
            
            new_task_data = self.get_serializer(new_task).data
        
        return Response({
            'interrupted_task': interrupted_task_data,
            'new_task': new_task_data,
            'message': 'Task switched successfully'
        })
    
    @extend_schema(
        tags=['tasks'],
        responses={
            200: OpenApiResponse(
                description='Current task or null if not tracking',
                response=TaskSerializer
            ),
        },
        description='Get the currently tracking task, or null if not tracking',
    )
    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        Get the currently tracking task.
        
        Returns null if user is not currently tracking anything.
        """
        current_task = Task.objects.filter(
            user=request.user,
            end_time__isnull=True
        ).first()
        
        if current_task:
            serializer = self.get_serializer(current_task)
            return Response(serializer.data)
        
        return Response(None)

