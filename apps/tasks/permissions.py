"""
Custom permissions for Task API.
"""
from rest_framework import permissions


class IsTaskOwnerOrAssignee(permissions.BasePermission):
    """
    Permission that allows:
    - Any authenticated user to view tasks (GET, HEAD, OPTIONS)
    - Any authenticated user to update tasks (PUT, PATCH)
    - Only creator or assignee to delete tasks (DELETE)
    """

    def has_permission(self, request, view):
        """
        Check if user is authenticated.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check object-level permissions.
        """
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True

        # Update permissions (PUT, PATCH) are allowed to any authenticated user
        if request.method in ['PUT', 'PATCH']:
            return True

        # Delete permission only for creator or assignee
        if request.method == 'DELETE':
            is_creator = obj.creator == request.user
            is_assignee = obj.assignee == request.user if obj.assignee else False
            return is_creator or is_assignee

        return False
