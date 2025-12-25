"""
Integration tests for User API endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from tests.conftest import assert_user_structure, assert_pagination_structure


@pytest.mark.integration
@pytest.mark.django_db
class TestUserAPI:
    """Test suite for User API endpoints."""

    def test_get_current_user(self, authenticated_client, user):
        """Test getting current authenticated user info."""
        url = reverse('user-current-user')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        # Check structure and values
        assert_user_structure(response.data, user_obj=user)

    def test_list_users(self, authenticated_client, user, another_user):
        """Test listing all users."""
        url = reverse('user-list')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        # Check pagination structure
        assert_pagination_structure(response.data)
        assert response.data['count'] >= 2

        # Check each user has correct structure
        for user_data in response.data['results']:
            assert_user_structure(user_data)

    def test_search_users_by_username(self, authenticated_client, user, another_user):
        """Test searching users by username."""
        url = reverse('user-list') + f'?search={user.username[:4]}'
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['uuid'] == str(user.uuid)
        assert response.data['results'][0]['username'] == user.username
        assert response.data['results'][0]['email'] == user.email

    def test_search_users_by_email(self, authenticated_client, user):
        """Test searching users by email."""
        url = reverse('user-list') + f'?search={user.email}'
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['uuid'] == str(user.uuid)
        assert response.data['results'][0]['email'] == user.email

    def test_retrieve_user(self, authenticated_client, user, another_user):
        """Test retrieving a specific user."""
        url = reverse('user-detail', kwargs={'uuid': another_user.uuid})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        # Check structure and values
        assert_user_structure(response.data, user_obj=another_user)

    def test_unauthenticated_access(self, api_client):
        """Test that unauthenticated users cannot access user endpoints."""
        url = reverse('user-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
