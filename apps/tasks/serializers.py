from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task, Comment

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_uuid = serializers.UUIDField(source='author.uuid', read_only=True)

    class Meta:
        model = Comment
        fields = ('uuid', 'author', 'author_uuid', 'text', 'created_at')
        read_only_fields = ('uuid', 'created_at')


class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(read_only=True)
    creator_uuid = serializers.UUIDField(source='creator.uuid', read_only=True)
    assignee = serializers.StringRelatedField(read_only=True)
    assignee_uuid = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
        write_only=True
    )
    assignee_details_uuid = serializers.UUIDField(source='assignee.uuid', read_only=True)

    class Meta:
        model = Task
        fields = (
            'uuid', 'title', 'description', 'creator', 'creator_uuid',
            'assignee', 'assignee_uuid', 'assignee_details_uuid',
            'is_completed', 'completed_at', 'created_at', 'updated_at'
        )
        read_only_fields = ('uuid', 'completed_at', 'created_at', 'updated_at')
