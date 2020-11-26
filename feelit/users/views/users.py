"""Users views."""

# Django REST Framework
from rest_framework import viewsets


# Permissions
from rest_framework.permissions import AllowAny

# Serializers
from feelit.users.serializers import (
    UserModelSerializer
)

# Models
from feelit.users.models import User


class UserViewSet(viewsets.ModelViewSet):
    """User view set."""

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'
    permission_classes = [AllowAny]
