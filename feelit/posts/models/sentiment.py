"""Sentiment model."""

# Django
from django.db import models

# Utilities
from feelit.utils.models import FeelitModel


class Sentiment(FeelitModel):
    """ Sentiment model

    Results from sentiment analysis. Obtained from Sentiment API Data model.
    """

    comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE, related_name='rated_comment')

    polarity = models.FloatField(null=True)
    subjetivity = models.FloatField(null=True)

    def __str__(self):
        """ Return comment and polarity result."""
        return '{} = {}'.format(self.comment.text, self.polarity)
