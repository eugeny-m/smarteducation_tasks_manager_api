from rest_framework import permissions

class IsCreatorOrAssignee(permissions.BasePermission):
    """
    Custom permission to only allow creators or assignees of a task to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the creator or assignee
        return obj.creator == request.user or obj.assignee == request.user
