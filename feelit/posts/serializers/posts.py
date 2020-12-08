"""Post serializer."""

# Django REST Framwork
from rest_framework import serializers

# Models
from feelit.posts.models import Post

# Serializer
from feelit.posts.serializers.comments import CommentPostSerializer


class PostModelSerializer(serializers.ModelSerializer):
    """ Post model serializer. """

    comments = CommentPostSerializer(many=True)

    class Meta:
        """Meta class."""

        model = Post
        fields = ('id', 'user', 'profile', 'title', 'photo', 'post_rating', 'comments')
        read_only_fields = ('id','user', 'profile', 'post_rating')

    def to_representation(self, instance):
        representation = super(PostModelSerializer, self).to_representation(instance)
        representation['user'] = instance.user.username
        return representation
        

class CreatePostSerializer(serializers.ModelSerializer):
    """Post model serializer."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    comments = serializers.StringRelatedField(many=True)
    
    class Meta:
        """Meta Class"""
        model = Post
        fields = ('user', 'title', 'photo', 'profile', 'comments')
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
