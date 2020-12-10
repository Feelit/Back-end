"""Sentiment serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from feelit.posts.models import Sentiment, Comment

# Utilities
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class CreateSentimentSerializer(serializers.ModelSerializer):
    """ Analyze the text from each comment, do GET request to API
    and bring results.
    """
    pass