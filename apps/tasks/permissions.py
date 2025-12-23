"""
Custom permissions for Task API.
"""
from rest_framework import permissions


class IsTaskOwnerOrAssignee(permissions.BasePermission):
    """
    Permission that allows:
    - Any authenticated user to view tasks (GET, HEAD, OPTIONS)
    - Creator or assignee to update tasks (PUT, PATCH)
    - Creator or assignee to delete tasks (DELETE)
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
        
        # Write permissions (PUT, PATCH, DELETE) only for creator or assignee
        is_creator = obj.creator == request.user
        is_assignee = obj.assignee == request.user if obj.assignee else False
        
        return is_creator or is_assignee
