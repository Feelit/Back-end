""" Posts admin."""

# Django
from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    """Post admin."""

    list_display = ('id', 'user__username', 'post_rating')
    list_filter = ('post_rating', 'created', 'modified')
