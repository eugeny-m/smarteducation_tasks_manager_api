"""
Admin configuration for Task and Comment models.
"""
from django.contrib import admin
from .models import Task, Comment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Task admin interface.
    """
    list_display = ['title', 'uuid', 'creator', 'assignee', 'is_completed',
                    'created_at']
    list_filter = ['is_completed', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'uuid', 'creator__username',
                     'assignee__username']
    readonly_fields = ['uuid', 'created_at', 'updated_at', 'completed_at']
    raw_id_fields = ['creator', 'assignee']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('uuid', 'title', 'description')
        }),
        ('Assignment', {
            'fields': ('creator', 'assignee')
        }),
        ('Status', {
            'fields': ('is_completed', 'completed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Comment admin interface.
    """
    list_display = ['__str__', 'uuid', 'task', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['text', 'uuid', 'task__title', 'author__username']
    readonly_fields = ['uuid', 'created_at', 'updated_at']
    raw_id_fields = ['task', 'author']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('uuid', 'task', 'author', 'text')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )