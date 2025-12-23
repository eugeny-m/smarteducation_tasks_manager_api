from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from .services import TaskService, CommentService
from .permissions import IsCreatorOrAssignee
from .filters import TaskFilter

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Task operations.
    """
    queryset = Task.objects.select_related('creator', 'assignee').all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrAssignee]
    lookup_field = 'uuid'
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = TaskFilter
    ordering_fields = ['created_at', 'updated_at', 'title', 'is_completed']
    ordering = ['-created_at']
    search_fields = ['title', 'description']

    @extend_schema(
        parameters=[
            OpenApiParameter(name='creator', type=str, description='Filter by creator UUID'),
            OpenApiParameter(name='assignee', type=str, description='Filter by assignee UUID'),
            OpenApiParameter(name='is_completed', type=bool, description='Filter by completion status'),
            OpenApiParameter(name='ordering', type=str, description='Order by field (e.g., -created_at)'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        task = TaskService.create_task(serializer.validated_data, creator=self.request.user)
        serializer.instance = task

    def perform_update(self, serializer):
        task = TaskService.update_task(self.get_object(), serializer.validated_data)
        serializer.instance = task


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment operations.
    Nested under tasks/{task_uuid}/comments/
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        task_uuid = self.kwargs.get('task_uuid')
        return Comment.objects.filter(task__uuid=task_uuid).select_related('author', 'task')

    def perform_create(self, serializer):
        task_uuid = self.kwargs.get('task_uuid')
        try:
            task = Task.objects.get(uuid=task_uuid)
        except Task.DoesNotExist:
            return Response({'detail': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        comment = CommentService.create_comment(
            serializer.validated_data,
            author=self.request.user,
            task=task
        )
        serializer.instance = comment
