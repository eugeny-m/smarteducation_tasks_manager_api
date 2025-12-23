"""
Filters for User model.
"""
from django.db import models
from django_filters import rest_framework as filters
from .models import User


class UserFilter(filters.FilterSet):
    """
    Filter for User model with search by username and email.
    """
    search = filters.CharFilter(method='filter_search', label='Search in username or email')

    class Meta:
        model = User
        fields = ['search']

    def filter_search(self, queryset, name, value):
        """
        Filter users by username or email containing the search value.
        """
        return queryset.filter(
            models.Q(username__icontains=value) |
            models.Q(email__icontains=value)
        )
