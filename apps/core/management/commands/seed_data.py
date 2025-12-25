"""
Management command to seed database with test data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.tasks.models import Task, Comment
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with test data (users, tasks, comments)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))
        self.stdout.write('')

        with transaction.atomic():
            # Create users
            self.stdout.write(self.style.WARNING('Creating users:'))
            self.stdout.write('=' * 60)

            users_data = [
                {
                    'username': 'admin',
                    'email': 'admin@example.com',
                    'password': 'admin123',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'is_superuser': True,
                    'is_staff': True,
                },
                {
                    'username': 'john_doe',
                    'email': 'john@example.com',
                    'password': 'john123',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'is_superuser': False,
                    'is_staff': False,
                },
                {
                    'username': 'jane_smith',
                    'email': 'jane@example.com',
                    'password': 'jane123',
                    'first_name': 'Jane',
                    'last_name': 'Smith',
                    'is_superuser': False,
                    'is_staff': False,
                },
                {
                    'username': 'bob_wilson',
                    'email': 'bob@example.com',
                    'password': 'bob123',
                    'first_name': 'Bob',
                    'last_name': 'Wilson',
                    'is_superuser': False,
                    'is_staff': False,
                },
            ]

            users = []
            for user_data in users_data:
                password = user_data.pop('password')
                is_superuser = user_data.pop('is_superuser')

                # Check if user already exists
                if User.objects.filter(username=user_data['username']).exists():
                    self.stdout.write(
                        self.style.WARNING(
                            f"  User '{user_data['username']}' already exists, skipping..."
                        )
                    )
                    user = User.objects.get(username=user_data['username'])
                    users.append(user)
                    continue

                if is_superuser:
                    user = User.objects.create_superuser(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=password,
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                    )
                else:
                    user = User.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=password,
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        is_staff=user_data['is_staff'],
                    )

                users.append(user)

                role = 'ADMIN' if is_superuser or user.is_staff else 'USER'
                self.stdout.write(
                    f"  ✓ Username: {user_data['username']:15} "
                    f"Password: {password:10} "
                    f"Email: {user_data['email']:20} "
                    f"Role: {role}"
                )

            self.stdout.write('')
            self.stdout.write(self.style.WARNING('Creating tasks:'))
            self.stdout.write('=' * 60)

            tasks_data = [
                {
                    'title': 'Setup development environment',
                    'description': 'Install all required dependencies and configure IDE',
                    'creator': users[0],  # admin
                    'assignee': users[1],  # john_doe
                    'is_completed': True,
                },
                {
                    'title': 'Design database schema',
                    'description': 'Create ERD diagram and define all tables and relationships',
                    'creator': users[0],  # admin
                    'assignee': users[2],  # jane_smith
                    'is_completed': True,
                },
                {
                    'title': 'Implement authentication API',
                    'description': 'Create JWT authentication endpoints and user registration',
                    'creator': users[1],  # john_doe
                    'assignee': users[1],  # john_doe
                    'is_completed': False,
                },
                {
                    'title': 'Write unit tests',
                    'description': 'Add comprehensive test coverage for all models and services',
                    'creator': users[1],  # john_doe
                    'assignee': users[3],  # bob_wilson
                    'is_completed': False,
                },
                {
                    'title': 'Create API documentation',
                    'description': 'Generate OpenAPI documentation with examples',
                    'creator': users[2],  # jane_smith
                    'assignee': users[2],  # jane_smith
                    'is_completed': False,
                },
                {
                    'title': 'Setup CI/CD pipeline',
                    'description': 'Configure automated testing and deployment',
                    'creator': users[0],  # admin
                    'assignee': None,
                    'is_completed': False,
                },
            ]

            tasks = []
            for task_data in tasks_data:
                task = Task.objects.create(**task_data)
                tasks.append(task)

                status_icon = '✓' if task.is_completed else '○'
                assignee_name = task.assignee.username if task.assignee else 'Unassigned'

                self.stdout.write(
                    f"  {status_icon} {task.title[:40]:40} "
                    f"Creator: {task.creator.username:12} "
                    f"Assignee: {assignee_name:12}"
                )

            self.stdout.write('')
            self.stdout.write(self.style.WARNING('Creating comments:'))
            self.stdout.write('=' * 60)

            comments_data = [
                {
                    'task': tasks[0],
                    'author': users[1],  # john_doe
                    'text': 'Environment is set up and ready to go!',
                },
                {
                    'task': tasks[0],
                    'author': users[0],  # admin
                    'text': 'Great job! Moving to the next phase.',
                },
                {
                    'task': tasks[1],
                    'author': users[2],  # jane_smith
                    'text': 'Initial schema design completed. Please review.',
                },
                {
                    'task': tasks[1],
                    'author': users[0],  # admin
                    'text': 'Looks good! Approved.',
                },
                {
                    'task': tasks[2],
                    'author': users[1],  # john_doe
                    'text': 'Working on JWT implementation. ETA: 2 days.',
                },
                {
                    'task': tasks[3],
                    'author': users[3],  # bob_wilson
                    'text': 'Started writing tests for user models.',
                },
                {
                    'task': tasks[4],
                    'author': users[2],  # jane_smith
                    'text': 'Using drf-spectacular for documentation generation.',
                },
                {
                    'task': tasks[5],
                    'author': users[0],  # admin
                    'text': 'Need to decide between GitHub Actions and GitLab CI.',
                },
            ]

            for comment_data in comments_data:
                comment = Comment.objects.create(**comment_data)
                self.stdout.write(
                    f"  ✓ Task: {comment.task.title[:30]:30} "
                    f"Author: {comment.author.username:12} "
                    f"Comment: {comment.text[:40]}..."
                )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users, {len(tasks)} tasks, {len(comments_data)} comments'))
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('You can now login with any of the users listed above.'))
