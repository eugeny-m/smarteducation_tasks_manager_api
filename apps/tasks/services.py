"""
Service layer for business logic related to tasks and comments.
"""
from django.utils import timezone
from .models import Task, Comment


class TaskService:
    """
    Service for Task-related operations.
    """
    
    @staticmethod
    def create_task(validated_data, creator):
        """
        Create a new task.

        Args:
            validated_data: Validated data from serializer
            creator: User instance who creates the task

        Returns:
            Task instance
        """
        # Remove assignee_uuid from validated_data
        validated_data.pop('assignee_uuid', None)
        validated_data['creator'] = creator
        task = Task.objects.create(**validated_data)
        return task
    
    @staticmethod
    def update_task(task, validated_data):
        """
        Update an existing task.
        Automatically sets completed_at when is_completed changes to True.

        Args:
            task: Task instance to update
            validated_data: Validated data from serializer

        Returns:
            Updated Task instance
        """
        # Remove assignee_uuid from validated_data
        validated_data.pop('assignee_uuid', None)

        # Check if is_completed is changing from False to True
        if 'is_completed' in validated_data:
            new_is_completed = validated_data['is_completed']
            old_is_completed = task.is_completed

            # Set completed_at only when transitioning to completed
            if new_is_completed and not old_is_completed:
                validated_data['completed_at'] = timezone.now()
            # Clear completed_at if unmarking as completed
            elif not new_is_completed and old_is_completed:
                validated_data['completed_at'] = None

        # Update task fields
        for field, value in validated_data.items():
            setattr(task, field, value)

        task.save()
        return task


class CommentService:
    """
    Service for Comment-related operations.
    """
    
    @staticmethod
    def create_comment(validated_data, author, task):
        """
        Create a new comment.

        Args:
            validated_data: Validated data from serializer
            author: User instance who creates the comment
            task: Task instance the comment belongs to

        Returns:
            Comment instance
        """
        validated_data['author'] = author
        validated_data['task'] = task
        comment = Comment.objects.create(**validated_data)
        return comment