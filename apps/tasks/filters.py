from django_filters import rest_framework as filters
from .models import Task

class TaskFilter(filters.FilterSet):
    creator = filters.UUIDFilter(field_name='creator__uuid')
    assignee = filters.UUIDFilter(field_name='assignee__uuid')
    is_completed = filters.BooleanFilter(field_name='is_completed')

    class Meta:
        model = Task
        fields = ['creator', 'assignee', 'is_completed']
