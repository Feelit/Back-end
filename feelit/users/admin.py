"""User models admin."""

# Django
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_verified')
    list_filter = ('is_staff', 'created', 'modified')