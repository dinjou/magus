from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import serializers

from magus.models import ScheduledExport


class ScheduledExportSerializer(serializers.ModelSerializer):
    """Serializer for scheduled exports"""
    
    class Meta:
        model = ScheduledExport
        fields = [
            'id',
            'frequency',
            'email_to',
            'is_active',
            'last_sent',
            'next_scheduled',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'last_sent', 'next_scheduled', 'created_at', 'updated_at']


@extend_schema_view(
    list=extend_schema(tags=['export'], description='List scheduled exports'),
    create=extend_schema(tags=['export'], description='Create scheduled export'),
    retrieve=extend_schema(tags=['export'], description='Get scheduled export'),
    update=extend_schema(tags=['export'], description='Update scheduled export'),
    partial_update=extend_schema(tags=['export'], description='Partially update scheduled export'),
    destroy=extend_schema(tags=['export'], description='Delete scheduled export'),
)
class ScheduledExportViewSet(viewsets.ModelViewSet):
    """ViewSet for managing scheduled exports"""
    
    serializer_class = ScheduledExportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter by current user"""
        return ScheduledExport.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set user when creating"""
        serializer.save(user=self.request.user)

