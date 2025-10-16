from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ProfileSerializer,
)


@extend_schema(
    tags=['auth'],
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            response=UserSerializer,
            description='User created successfully. Returns user data and JWT tokens.'
        ),
        400: OpenApiResponse(description='Validation error'),
    },
    description='Register a new user account. Automatically creates profile and default task types.',
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user.
    
    Creates a new user account, profile, and default task types.
    Returns user data along with JWT access and refresh tokens.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['auth'],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string'},
                'password': {'type': 'string'},
            },
            'required': ['username', 'password']
        }
    },
    responses={
        200: OpenApiResponse(description='Login successful, returns JWT tokens'),
        401: OpenApiResponse(description='Invalid credentials'),
    },
    description='Authenticate user and receive JWT tokens',
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login with username and password.
    
    Returns JWT access and refresh tokens on successful authentication.
    """
    from django.contrib.auth import authenticate
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@extend_schema(
    tags=['auth'],
    responses={
        200: OpenApiResponse(description='Logout successful'),
    },
    description='Logout current user (client should delete tokens)',
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout user.
    
    Note: With JWT, logout is primarily handled client-side by deleting tokens.
    This endpoint is provided for consistency but doesn't invalidate the token server-side.
    """
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@extend_schema(
    tags=['profile'],
    responses={
        200: ProfileSerializer,
    },
    description='Get current user profile',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_detail_view(request):
    """Get current user's profile"""
    profile = request.user.profile
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)


@extend_schema(
    tags=['profile'],
    request=ProfileSerializer,
    responses={
        200: ProfileSerializer,
        400: OpenApiResponse(description='Validation error'),
    },
    description='Update current user profile settings',
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def profile_update_view(request):
    """Update current user's profile"""
    profile = request.user.profile
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['profile'],
    responses={
        204: OpenApiResponse(description='Account deleted successfully'),
    },
    description='Delete current user account and all associated data (GDPR compliance)',
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def profile_delete_view(request):
    """
    Delete current user account.
    
    This will cascade delete all user data:
    - Profile
    - Task types
    - Tasks
    - API keys
    - Scheduled exports
    
    This action is irreversible!
    """
    user = request.user
    user.delete()
    return Response(
        {'message': 'Account deleted successfully'},
        status=status.HTTP_204_NO_CONTENT
    )


@extend_schema(
    tags=['auth'],
    responses={
        200: OpenApiResponse(
            description='Current authenticated user information',
            response=UserSerializer
        ),
        401: OpenApiResponse(description='Not authenticated'),
    },
    description='Get current authenticated user information',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """Get current authenticated user"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

