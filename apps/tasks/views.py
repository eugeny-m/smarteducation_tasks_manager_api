"""
ViewSets for Task and Comment APIs.
"""
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from .services import TaskService, CommentService
from .permissions import IsTaskOwnerOrAssignee
from .filters import TaskFilter


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Task CRUD operations.
    Uses UUID for lookup instead of primary key.
    """
    queryset = Task.objects.select_related('creator', 'assignee').all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskOwnerOrAssignee]
    lookup_field = 'uuid'
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TaskFilter
    ordering_fields = ['created_at', 'updated_at', 'title', 'is_completed']
    ordering = ['-created_at']
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='creator', type=str,
                             description='Filter by creator UUID'),
            OpenApiParameter(name='assignee', type=str,
                             description='Filter by assignee UUID'),
            OpenApiParameter(name='is_completed', type=bool,
                             description='Filter by completion status'),
            OpenApiParameter(name='ordering', type=str,
                             description='Order by field (e.g., -created_at)'),
        ]
    )
    def list(self, request, *args, **kwargs):
        """List all tasks with filtering and pagination."""
        return super().list(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """
        Create a new task using TaskService.
        """
        validated_data = serializer.validated_data
        task = TaskService.create_task(validated_data,
                                       creator=self.request.user)
        serializer.instance = task
    
    def perform_update(self, serializer):
        """
        Update a task using TaskService.
        """
        validated_data = serializer.validated_data
        task = TaskService.update_task(self.get_object(), validated_data)
        serializer.instance = task


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment operations.
    Only supports create and list operations.
    Nested under tasks/{task_uuid}/comments/
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'
    http_method_names = ['get', 'post', 'head',
                         'options']  # Only allow GET and POST
    
    def get_queryset(self):
        """
        Get comments for a specific task.
        """
        task_uuid = self.kwargs.get('task_uuid')
        return Comment.objects.filter(task__uuid=task_uuid).select_related(
            'author', 'task')
    
    def perform_create(self, serializer):
        """
        Create a new comment using CommentService.
        """
        task_uuid = self.kwargs.get('task_uuid')
        
        # Get task by UUID
        try:
            task = Task.objects.get(uuid=task_uuid)
        except Task.DoesNotExist:
            return Response(
                {'detail': 'Task not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        validated_data = serializer.validated_data
        comment = CommentService.create_comment(
            validated_data,
            author=self.request.user,
            task=task
        )
        serializer.instance = comment
