"""
Filter backends for Task API.
"""
import django_filters
from apps.users.models import User
from .models import Task


class TaskFilter(django_filters.FilterSet):
    """
    Filter class for Task model.
    Filters by creator UUID, assignee UUID, and completion status.
    """
    creator = django_filters.UUIDFilter(method='filter_by_creator_uuid')
    assignee = django_filters.UUIDFilter(method='filter_by_assignee_uuid')
    is_completed = django_filters.BooleanFilter(field_name='is_completed')
    
    class Meta:
        model = Task
        fields = ['creator', 'assignee', 'is_completed']
    
    def filter_by_creator_uuid(self, queryset, name, value):
        """
        Filter tasks by creator UUID.
        """
        try:
            user = User.objects.get(uuid=value)
            return queryset.filter(creator=user)
        except User.DoesNotExist:
            return queryset.none()
    
    def filter_by_assignee_uuid(self, queryset, name, value):
        """
        Filter tasks by assignee UUID.
        """
        try:
            user = User.objects.get(uuid=value)
            return queryset.filter(assignee=user)
        except User.DoesNotExist:
            return queryset.none()
