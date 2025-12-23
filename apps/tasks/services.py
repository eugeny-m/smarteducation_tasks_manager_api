from django.utils import timezone
from .models import Task, Comment

class TaskService:
    @staticmethod
    def create_task(validated_data, creator):
        """
        Business logic for creating a task.
        """
        # Resolve assignee from assignee_uuid if provided
        assignee = validated_data.pop('assignee_uuid', None)
        if assignee:
            validated_data['assignee'] = assignee
            
        return Task.objects.create(creator=creator, **validated_data)

    @staticmethod
    def update_task(task, validated_data):
        """
        Business logic for updating a task.
        """
        # Handle is_completed timestamp
        if 'is_completed' in validated_data:
            if validated_data['is_completed'] and not task.is_completed:
                task.completed_at = timezone.now()
            elif not validated_data['is_completed']:
                task.completed_at = None

        # Resolve assignee from assignee_uuid if provided
        assignee = validated_data.pop('assignee_uuid', None)
        if assignee:
            task.assignee = assignee

        for attr, value in validated_data.items():
            setattr(task, attr, value)
        
        task.save()
        return task


class CommentService:
    @staticmethod
    def create_comment(validated_data, author, task):
        """
        Business logic for creating a comment.
        """
        return Comment.objects.create(
            author=author,
            task=task,
            **validated_data
        )
