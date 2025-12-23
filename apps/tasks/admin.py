from django.contrib import admin
from .models import Task, Comment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'assignee', 'is_completed', 'uuid', 'created_at')
    list_filter = ('is_completed', 'created_at')
    search_fields = ('title', 'description', 'uuid')
    readonly_fields = ('uuid', 'created_at', 'updated_at', 'completed_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'uuid', 'created_at')
    search_fields = ('text', 'uuid')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
