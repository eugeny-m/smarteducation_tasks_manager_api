"""
Views for user authentication and profile.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import User
from .serializers import UserSerializer
from .filters import UserFilter


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving users.
    Supports filtering by username or email via 'search' query parameter.
    Uses UUID for lookup instead of primary key.
    """
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = UserFilter
    lookup_field = 'uuid'

    @extend_schema(
        responses={200: UserSerializer},
        description="Get current authenticated user information"
    )
    @action(detail=False, methods=['get'], url_path='me')
    def current_user(self, request):
        """
        Get information about the currently authenticated user.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
