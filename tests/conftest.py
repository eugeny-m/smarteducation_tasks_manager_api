"""
Pytest configuration and fixtures for integration tests.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.tasks.models import Task

User = get_user_model()


# Expected API response structures
TASK_FIELDS = {
    'uuid', 'title', 'description', 'creator', 'assignee',
    'is_completed', 'completed_at', 'created_at', 'updated_at'
}

USER_FIELDS = {
    'uuid', 'username', 'email', 'first_name', 'last_name'
}

PAGINATION_FIELDS = {
    'count', 'next', 'previous', 'results'
}


@pytest.fixture
def api_client():
    """
    Fixture for DRF API client.
    """
    return APIClient()


@pytest.fixture
def user(db):
    """
    Fixture for creating a regular user.
    """
    return User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def another_user(db):
    """
    Fixture for creating another user for multi-user tests.
    """
    return User.objects.create_user(
        username='anotheruser',
        email='anotheruser@example.com',
        password='testpass123',
        first_name='Another',
        last_name='User'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """
    Fixture for authenticated API client.
    """
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_user(db):
    """
    Fixture for creating an admin user.
    """
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )


@pytest.fixture
def admin_client(api_client, admin_user):
    """
    Fixture for authenticated admin API client.
    """
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def task_data():
    """
    Fixture with base task data for creating tasks.
    """
    return {
        'title': 'Test Task',
        'description': 'Test Description',
    }


@pytest.fixture
def task(db, user, task_data):
    """
    Fixture for creating a task instance.
    """
    return Task.objects.create(
        creator=user,
        **task_data
    )


def assert_task_structure(task_data, user_obj=None, assignee_obj=None):
    """
    Helper function to assert task response has correct structure and values.

    Args:
        task_data: Response data from API
        user_obj: Expected creator User object (optional)
        assignee_obj: Expected assignee User object (optional)
    """
    # Check all required fields are present
    assert set(task_data.keys()) == TASK_FIELDS

    # Check creator structure if provided
    if user_obj:
        assert_user_structure(task_data['creator'])
        assert task_data['creator']['uuid'] == str(user_obj.uuid)
        assert task_data['creator']['username'] == user_obj.username
        assert task_data['creator']['email'] == user_obj.email

    # Check assignee structure if provided
    if assignee_obj:
        assert task_data['assignee'] is not None
        assert_user_structure(task_data['assignee'])
        assert task_data['assignee']['uuid'] == str(assignee_obj.uuid)
        assert task_data['assignee']['username'] == assignee_obj.username
    elif assignee_obj is None and 'assignee' in task_data:
        assert task_data['assignee'] is None


def assert_user_structure(user_data, user_obj=None):
    """
    Helper function to assert user response has correct structure and values.

    Args:
        user_data: Response data from API
        user_obj: Expected User object (optional)
    """
    # Check all required fields are present
    assert set(user_data.keys()) == USER_FIELDS

    # Ensure sensitive fields are not exposed
    assert 'password' not in user_data
    assert 'is_staff' not in user_data
    assert 'is_superuser' not in user_data

    # Check values if user object provided
    if user_obj:
        assert user_data['uuid'] == str(user_obj.uuid)
        assert user_data['username'] == user_obj.username
        assert user_data['email'] == user_obj.email
        assert user_data['first_name'] == user_obj.first_name
        assert user_data['last_name'] == user_obj.last_name


def assert_pagination_structure(response_data):
    """
    Helper function to assert pagination structure.

    Args:
        response_data: Response data from API
    """
    assert set(response_data.keys()) == PAGINATION_FIELDS
    assert isinstance(response_data['results'], list)
