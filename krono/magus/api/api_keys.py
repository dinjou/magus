from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from magus.models import APIKey


class APIKeySerializer(serializers.ModelSerializer):
    """Serializer for API keys - never shows full key except on creation"""
    
    class Meta:
        model = APIKey
        fields = [
            'id',
            'name',
            'key_prefix',
            'created_at',
            'last_used',
            'is_active',
            'can_read',
            'can_write',
        ]
        read_only_fields = ['id', 'key_prefix', 'created_at', 'last_used']


class APIKeyCreateSerializer(serializers.Serializer):
    """Serializer for creating API keys"""
    
    name = serializers.CharField(max_length=100)
    can_read = serializers.BooleanField(default=True)
    can_write = serializers.BooleanField(default=True)


@extend_schema_view(
    list=extend_schema(
        tags=['api-keys'],
        description='List all API keys for current user (key_prefix only)',
    ),
    retrieve=extend_schema(
        tags=['api-keys'],
        description='Get API key details (key_prefix only)',
    ),
    destroy=extend_schema(
        tags=['api-keys'],
        description='Revoke (delete) an API key',
    ),
)
class APIKeyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user API keys.
    
    Note: Full API key is only shown once upon creation.
    """
    serializer_class = APIKeySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']  # No PUT/PATCH
    
    def get_queryset(self):
        """Filter by current user"""
        return APIKey.objects.filter(user=self.request.user)
    
    @extend_schema(
        request=APIKeyCreateSerializer,
        responses={
            201: OpenApiResponse(
                description='API key created. Full key returned ONCE.',
                response={
                    'type': 'object',
                    'properties': {
                        'api_key': {'type': 'string', 'description': 'Full API key - save this!'},
                        'key_prefix': {'type': 'string'},
                        'name': {'type': 'string'},
                        'id': {'type': 'integer'},
                    }
                }
            ),
        },
        tags=['api-keys'],
        description='Generate a new API key. Full key shown ONLY ONCE!',
    )
    def create(self, request):
        """
        Generate a new API key.
        
        The full key is only shown in this response. Save it immediately!
        """
        serializer = APIKeyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Generate key
        full_key = APIKey.generate_key()
        key_hash = APIKey.hash_key(full_key)
        key_prefix = full_key[:8]
        
        # Create API key
        api_key = APIKey.objects.create(
            user=request.user,
            name=serializer.validated_data['name'],
            key_prefix=key_prefix,
            key_hash=key_hash,
            can_read=serializer.validated_data.get('can_read', True),
            can_write=serializer.validated_data.get('can_write', True),
        )
        
        return Response({
            'api_key': full_key,  # Full key - ONLY shown once!
            'key_prefix': key_prefix,
            'name': api_key.name,
            'id': api_key.id,
            'message': 'API key created successfully. Save it now - it will not be shown again!',
        }, status=status.HTTP_201_CREATED)

