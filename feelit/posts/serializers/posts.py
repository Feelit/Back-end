"""Post serializer."""

# Django REST Framwork
from rest_framework import serializers

# Models
from feelit.users.models import User
from feelit.posts.models import Post


class PostModelSerializer(serializers.ModelSerializer):
    """Post model serializer"""

    class Meta:
        """Meta Class"""
        model = Post
        fields = '__all__'
