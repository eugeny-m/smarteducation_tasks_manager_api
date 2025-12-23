from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = ('uuid', 'username', 'email', 'first_name', 'last_name', 'created_at')
        read_only_fields = ('uuid', 'created_at')
