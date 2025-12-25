"""
Integration tests for Task API endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from apps.tasks.models import Task
from tests.conftest import assert_task_structure, assert_pagination_structure


@pytest.mark.integration
@pytest.mark.django_db
class TestTaskAPI:
    """Test suite for Task API endpoints."""

    def test_create_task(self, authenticated_client, user, task_data):
        """Test creating a new task."""
        url = reverse('task-list')

        response = authenticated_client.post(url, task_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        # Check structure and values
        assert_task_structure(response.data, user_obj=user)
        assert response.data['title'] == task_data['title']
        assert response.data['description'] == task_data['description']
        assert response.data['is_completed'] is False
        assert response.data['completed_at'] is None
        assert response.data['assignee'] is None

    def test_create_task_with_assignee(self, authenticated_client, user, another_user, task_data):
        """Test creating a task with an assignee."""
        url = reverse('task-list')
        data = {
            **task_data,
            'assignee_uuid': str(another_user.uuid),
        }

        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        # Check structure with assignee
        assert_task_structure(response.data, user_obj=user, assignee_obj=another_user)

        # Ensure assignee_uuid is not in response (write-only field)
        assert 'assignee_uuid' not in response.data

    def test_list_tasks(self, authenticated_client, user, task_data):
        """Test listing tasks."""
        Task.objects.create(creator=user, title='Task 1', description='Description 1')
        Task.objects.create(creator=user, title='Task 2', description='Description 2')

        url = reverse('task-list')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        # Check pagination structure
        assert_pagination_structure(response.data)
        assert response.data['count'] == 2
        assert len(response.data['results']) == 2

        # Check each task has correct structure
        for task in response.data['results']:
            assert_task_structure(task)

    def test_retrieve_task(self, authenticated_client, user, task):
        """Test retrieving a specific task."""
        url = reverse('task-detail', kwargs={'uuid': task.uuid})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        # Check structure and values
        assert_task_structure(response.data, user_obj=user)
        assert response.data['uuid'] == str(task.uuid)
        assert response.data['title'] == task.title
        assert response.data['description'] == task.description

    def test_update_task(self, authenticated_client, user):
        """Test updating a task."""
        task = Task.objects.create(
            title='Original Title',
            description='Original Description',
            creator=user
        )

        url = reverse('task-detail', kwargs={'uuid': task.uuid})
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
        }

        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'
        assert response.data['description'] == 'Updated Description'

    def test_complete_task(self, authenticated_client, user):
        """Test marking a task as completed."""
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            creator=user
        )

        url = reverse('task-detail', kwargs={'uuid': task.uuid})
        data = {'is_completed': True}

        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_completed'] is True
        assert response.data['completed_at'] is not None

        # Verify completed_at is a valid datetime string
        from datetime import datetime
        completed_at = response.data['completed_at']
        assert completed_at is not None
        # Should be ISO 8601 format
        datetime.fromisoformat(completed_at.replace('Z', '+00:00'))

    def test_delete_task(self, authenticated_client, user):
        """Test deleting a task."""
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            creator=user
        )

        url = reverse('task-detail', kwargs={'uuid': task.uuid})
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Task.objects.filter(uuid=task.uuid).exists()

    def test_unauthenticated_access(self, api_client):
        """Test that unauthenticated users cannot access tasks."""
        url = reverse('task-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_filter_tasks_by_completion(self, authenticated_client, user):
        """Test filtering tasks by completion status."""
        completed_task = Task.objects.create(
            title='Completed Task',
            description='Completed Description',
            creator=user,
            is_completed=True
        )
        Task.objects.create(
            title='Pending Task',
            description='Pending Description',
            creator=user,
            is_completed=False
        )

        url = reverse('task-list') + '?is_completed=true'
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['uuid'] == str(completed_task.uuid)
        assert response.data['results'][0]['title'] == 'Completed Task'
        assert response.data['results'][0]['description'] == 'Completed Description'
        assert response.data['results'][0]['is_completed'] is True

    def test_filter_tasks_by_creator(self, authenticated_client, user, another_user):
        """Test filtering tasks by creator UUID."""
        user_task = Task.objects.create(
            title='User Task',
            description='Created by user',
            creator=user
        )
        Task.objects.create(
            title='Another User Task',
            description='Created by another user',
            creator=another_user
        )

        url = reverse('task-list') + f'?creator={user.uuid}'
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['uuid'] == str(user_task.uuid)
        assert response.data['results'][0]['creator']['uuid'] == str(user.uuid)
        assert response.data['results'][0]['creator']['email'] == user.email

    def test_filter_tasks_by_assignee(self, authenticated_client, user, another_user):
        """Test filtering tasks by assignee UUID."""
        assigned_task = Task.objects.create(
            title='Assigned Task',
            description='Assigned to another user',
            creator=user,
            assignee=another_user
        )
        Task.objects.create(
            title='Unassigned Task',
            description='No assignee',
            creator=user
        )

        url = reverse('task-list') + f'?assignee={another_user.uuid}'
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['uuid'] == str(assigned_task.uuid)
        assert response.data['results'][0]['assignee']['uuid'] == str(another_user.uuid)
        assert response.data['results'][0]['assignee']['email'] == another_user.email
