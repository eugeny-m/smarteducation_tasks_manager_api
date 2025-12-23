"""
Serializers for Task and Comment models.
"""
from rest_framework import serializers
from django.utils import timezone
from apps.users.serializers import UserSerializer
from apps.users.models import User
from .models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    Handles UUID-based assignee field for API requests.
    """
    creator = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    assignee_uuid = serializers.UUIDField(
        write_only=True,
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model = Task
        fields = [
            'uuid',
            'title',
            'description',
            'creator',
            'assignee',
            'assignee_uuid',
            'is_completed',
            'completed_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'uuid',
            'creator',
            'assignee',
            'completed_at',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        """
        Object-level validation to set assignee from assignee_uuid.
        """
        assignee_uuid = attrs.get('assignee_uuid', None)
        if assignee_uuid is None:
            return attrs
        try:
            attrs['assignee'] = User.objects.get(uuid=assignee_uuid)
        except User.DoesNotExist:
            raise serializers.ValidationError( "User with this UUID does not exist.")
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    """
    author = UserSerializer(read_only=True)
    task_uuid = serializers.UUIDField(source='task.uuid', read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'uuid',
            'task_uuid',
            'author',
            'text',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['uuid', 'task_uuid', 'author', 'created_at', 'updated_at']
