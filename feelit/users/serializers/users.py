"""Users serializers."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from feelit.users.models import User

class UserModelSerialzier(serializers.ModelSerializer):
    """User model serializer."""
    
    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )