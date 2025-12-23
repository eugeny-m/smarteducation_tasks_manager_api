"""
URL routing for tasks and comments.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import TaskViewSet, CommentViewSet

# Main router for tasks
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

# Nested router for comments under tasks
tasks_router = routers.NestedDefaultRouter(router, r'tasks', lookup='task')
tasks_router.register(r'comments', CommentViewSet, basename='task-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(tasks_router.urls)),
]
