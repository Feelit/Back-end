"""Post serializer."""

# Django REST Framwork
from rest_framework import serializers

# Models
from feelit.posts.models import Post

# Serializer
from feelit.posts.serializers.comments import CommentPostSerializer


class PostModelSerializer(serializers.ModelSerializer):
    """ Post model serializer. """
  
    class Meta:
        """Meta class."""

        model = Post
        fields = ('user', 'profile', 'title', 'photo', 'post_rating')
        read_only_fields = ('user', 'profile', 'post_rating')


class CreatePostSerializer(serializers.ModelSerializer):
    """Post model serializer."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        """Meta Class"""
        model = Post
        fields = ('user', 'title', 'photo', 'profile')
        read_only_fields = ('user', 'profile', 'post_rating')

    def validate(self, data):
        """ Validate.

        Verify that the person who made the post is the account owner and is active.
        """
        if self.context['request'].user != data['user']:
            raise serializers.ValidationError('Post on behalf of others are not allowed')
        user = data['user']
        if not user.is_active:
            raise serializers.ValidationError('User account is inactive')
        return data

    def create(self, data):
        """ Create ride."""
        user = data['user']
        profile = user.profile
        post = Post.objects.create(**data, profile=profile)

        return post
