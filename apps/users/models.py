"""
User model extending Django's AbstractUser with BaseModel.
"""
from django.contrib.auth.models import AbstractUser
from apps.core.models import BaseModel


class User(AbstractUser, BaseModel):
    """
    Custom User model with UUID support.
    Inherits all fields from AbstractUser and BaseModel.
    """
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username
