""" Posts views."""

# Django
from django.core import exceptions

# Django REST Framework
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

# Models
from feelit.posts.models import Post
from feelit.users.models import User

# Serializers
from feelit.posts.serializers import (
    CreatePostSerializer,
    PostModelSerializer
)


class UserPostViewSet(viewsets.ModelViewSet):
    """ User Post viewset

    Manages posts actions for specific user.
    """

    def dispatch(self, request, *args, **kwargs):
        """ Verify username exists."""
        username = kwargs['username']
        self.user = get_object_or_404(User, username=username)
        return super(UserPostViewSet, self).dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        """ Add user and profile to serializer context."""
        context = super(UserPostViewSet, self).get_serializer_context()
        context['user'] = self.user
        context['profile'] = self.user.profile
        return context

    def get_serializer_class(self):
        """ Return serializer based on action."""
        if self.action == 'create':
            return CreatePostSerializer
        return PostModelSerializer

    def get_queryset(self):
        """ Return users posts."""
        return self.user.post_set


class PostViewSet(viewsets.ModelViewSet):
    """ General Post viewset

    List all public posts.
    """
    serializer_class = PostModelSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
