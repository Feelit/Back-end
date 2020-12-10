"""Comments serializers."""

# Django
from django.db.models import Avg

# Django REST Framework
from rest_framework import serializers

# Models
from feelit.users.models import User
from feelit.posts.models import Post, Comment, Sentiment

# Utilities
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class CreateCommentPostSerializer(serializers.ModelSerializer):
    """Create comments serializer."""

    text = serializers.CharField()

    class Meta:
        """Meta class."""
        model = Comment
        fields = ('text', 'comment_rating')
        readonlyfields = ('comment_rating')

    def validate(self, data):
        """ Validate user is logged and active."""
        user = self.context['request'].user
        if not user.is_verified:
            raise serializers.ValidationError('User must log in to comment')
        return data

    def create(self, data):
        """ Create comment."""
        for_user = self.context['post'].user

        rating = self.get_analysis(data)

        #rating = Sentiment.objects.filter(
        #    comment=self.context['comment']
        #)['polarity']

        Comment.objects.create(
            post=self.context['post'],
            from_user=self.context['request'].user,
            for_user=for_user,
            comment_rating=rating,
            **data
        )

        # Post rating update
        post_rating = round(
            Comment.objects.filter(
                post=self.context['post']
            ).aggregate(Avg('comment_rating'))['comment_rating__avg'],
            1
        )

        self.context['post'].post_rating = post_rating
        self.context['post'].save()

        # Profile rating update
        user_avg = round(
            Post.objects.filter(
                user=for_user
            ).aggregate(Avg('post_rating'))['post_rating__avg'],
            1
        )

        for_user.profile.profile_rating = user_avg
        for_user.profile.save()

        return self.context['post']

    def get_analysis(self, data):
        """ Get data sentiment analysis. """
        text = self.data['text']
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        response = session.get('https://sentimentapi-oqblqthtkq-ue.a.run.app/api/v1/analyzer/?comment=' + text)
        analysis = response.json()
        polarity = analysis['polarity']
        subjectivity = analysis['subjectivity']

        #Sentiment.objects.create(
        #    polarity=polarity,
        #    subjetivity=subjectivity
        #)
        return polarity


class CommentPostSerializer(serializers.ModelSerializer):
    """ Comments model serializer."""

    class Meta:
        """ Meta Class."""
        model = Comment
        fields = ('text', 'from_user', 'comment_rating')

    def to_representation(self, instance):
        representation = super(CommentPostSerializer, self).to_representation(instance)
        representation['from_user'] = instance.from_user.username
        return representation
