from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from magus.models import Profile, TaskType, Task


class UserSerializer(serializers.ModelSerializer):
    """Basic user information serializer"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    """User registration serializer with password validation"""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Confirm password'
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate_email(self, value):
        """Ensure email is unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, attrs):
        """Ensure passwords match"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """Create user with hashed password"""
        try:
            validated_data.pop('password2')
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', '')
            )
            return user
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"User creation error: {str(e)}", exc_info=True)
            raise serializers.ValidationError(f"User creation failed: {str(e)}")


class ProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'user',
            'email_for_exports',
            'timezone',
            'theme',
            'long_press_duration',
            'pinned_tasks_visible',
            'enable_live_activities',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def validate_long_press_duration(self, value):
        """Ensure long press duration is reasonable"""
        if value < 0.5 or value > 5.0:
            raise serializers.ValidationError(
                "Long press duration must be between 0.5 and 5.0 seconds."
            )
        return value
    
    def validate_pinned_tasks_visible(self, value):
        """Ensure pinned tasks count is reasonable"""
        if value < 1 or value > 12:
            raise serializers.ValidationError(
                "Pinned tasks visible must be between 1 and 12."
            )
        return value


class TaskTypeSerializer(serializers.ModelSerializer):
    """Task type serializer"""
    
    class Meta:
        model = TaskType
        fields = [
            'id',
            'name',
            'emoji',
            'color',
            'is_pinned',
            'is_archived',
            'sort_order',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    """Task serializer with nested task type"""
    
    task_type_detail = TaskTypeSerializer(source='task_type', read_only=True)
    task_type = serializers.PrimaryKeyRelatedField(
        queryset=TaskType.objects.none(),  # Will be set in view
        write_only=True
    )
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = [
            'id',
            'task_type',
            'task_type_detail',
            'start_time',
            'end_time',
            'duration',
            'interrupted',
            'is_manual_entry',
            'notes',
            'edited_by_user',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'duration']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set queryset for task_type based on request user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            self.fields['task_type'].queryset = TaskType.objects.filter(
                user=request.user,
                is_archived=False
            )
    
    def get_duration(self, obj):
        """Calculate duration in seconds"""
        return obj.duration
    
    def validate(self, attrs):
        """Validate task times"""
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        
        if end_time and start_time and end_time <= start_time:
            raise serializers.ValidationError(
                {"end_time": "End time must be after start time."}
            )
        
        return attrs


class TaskCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating tasks via tracking actions"""
    
    task_type = serializers.PrimaryKeyRelatedField(
        queryset=TaskType.objects.none()
    )
    
    class Meta:
        model = Task
        fields = ['task_type', 'notes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            self.fields['task_type'].queryset = TaskType.objects.filter(
                user=request.user,
                is_archived=False
            )

