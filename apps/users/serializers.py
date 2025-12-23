"""
Serializers for User model.
"""
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Used for nested representation in Task and Comment serializers.
    """
    
    class Meta:
        model = User
        fields = ['uuid', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = fields
