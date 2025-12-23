"""
Admin configuration for User model.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin with UUID field display.
    """
    list_display = ['username', 'email', 'uuid', 'first_name', 'last_name',
                    'is_staff', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'uuid']
    readonly_fields = ['uuid', 'created_at', 'updated_at', 'last_login',
                       'date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('uuid', 'created_at', 'updated_at')
        }),
    )
