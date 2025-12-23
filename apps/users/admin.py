from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'uuid', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'uuid')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('uuid', 'created_at', 'updated_at')}),
    )
