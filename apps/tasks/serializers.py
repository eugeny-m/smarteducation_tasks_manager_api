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
    assignee_uuid = serializers.UUIDField(write_only=True, required=False,
                                          allow_null=True)
    
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
        read_only_fields = ['uuid', 'creator', 'assignee', 'completed_at',
                            'created_at', 'updated_at']
    
    def validate_assignee_uuid(self, value):
        """
        Validate that the assignee UUID corresponds to an existing user.
        """
        if value is None:
            return None
        
        try:
            user = User.objects.get(uuid=value)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with this UUID does not exist.")
    
    def create(self, validated_data):
        """
        Create a new task.
        Assignee object is already validated and converted from UUID.
        """
        # Extract assignee object from validated data
        assignee = validated_data.pop('assignee_uuid', None)
        
        # Set assignee if provided
        if assignee:
            validated_data['assignee'] = assignee
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Update a task.
        Assignee object is already validated and converted from UUID.
        """
        # Extract assignee object from validated data
        assignee = validated_data.pop('assignee_uuid', None)
        
        # Update assignee if provided
        if 'assignee_uuid' in self.initial_data:
            validated_data['assignee'] = assignee
        
        return super().update(instance, validated_data)


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
