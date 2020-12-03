""" Posts views."""

# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Models
from feelit.posts.models import Post
from feelit.users.models import User

# Serializers
from feelit.posts.serializers import (
    CreatePostSerializer,
    PostModelSerializer,
    CreateCommentPostSerializer
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
        if self.action in ['comment']:
            return CreateCommentPostSerializer
        return PostModelSerializer

    def get_queryset(self):
        """ Return users posts."""
        return self.user.post_set

    @action(detail=True, methods=['post'])
    def comment(self, request, *args, **kwargs):
        """ Add new comment to the post."""
        post = self.get_object()
        serializer_class = CreateCommentPostSerializer
        context = self.get_serializer_context()
        context['post'] = post
        serializer = serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        data = PostModelSerializer(post).data
        return Response(data, status=status.HTTP_201_CREATED)

 
class PostViewSet(viewsets.ModelViewSet):
    """ General Post viewset

    List all public posts.
    """
    serializer_class = PostModelSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
