"""Users views."""

# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


# Permissions
from rest_framework.permissions import AllowAny

# Serializers
from feelit.users.serializers import (
    AccountVerificationSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    UserLoginSerializer
)

# Models
from feelit.users.models import User


class UserViewSet(viewsets.ModelViewSet):
    """User view set

    Handle Sign up and Login
    """

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up.""" 
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """ Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulations, now you are part of Feel It!'}
        return Response(data, status=status.HTTP_200_OK)
