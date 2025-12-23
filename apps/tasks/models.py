"""
Task and Comment models.
"""
from django.db import models
from django.conf import settings
from apps.core.models import BaseModel


class Task(BaseModel):
    """
    Task model for managing user tasks.
    """
    title = models.CharField(max_length=255, help_text="Task title")
    description = models.TextField(blank=True, help_text="Task description")
    
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        help_text="User who created the task"
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='assigned_tasks',
        null=True,
        blank=True,
        help_text="User assigned to the task"
    )
    
    is_completed = models.BooleanField(default=False,
                                       help_text="Task completion status")
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when task was marked as completed"
    )
    
    class Meta:
        db_table = 'tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['creator']),
            models.Index(fields=['assignee']),
            models.Index(fields=['is_completed']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.uuid})"


class Comment(BaseModel):
    """
    Comment model for task discussions.
    """
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="Task this comment belongs to"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="User who wrote the comment"
    )
    text = models.TextField(help_text="Comment text")
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['task']),
            models.Index(fields=['author']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.title}"