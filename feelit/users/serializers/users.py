"""Users serializers."""

# Django
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from feelit.users.models import User, Profile

# Serializers
from feelit.users.serializers.profiles import ProfileModelSerializer

# Utilities
import jwt
from datetime import timedelta


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'email',
            'profile'
        )


class UserSignUpSerializer(serializers.Serializer):
    """ User sign up serializer.

    Handle sign up data validation and user/profile creation.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    first_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """ Verify passwords match. """

        passwd = data['password']
        passwd_confirm = data['password_confirmation']
        if passwd != passwd_confirm:
            raise serializers.ValidationError("Passwords don't match")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """ Handle user create."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=True)
        Profile.objects.create(user=user)
        #self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        """ Send account verification link to given user."""
        verification_token = self.gen_verification_token(user)
        subject = 'Welcome {}! Verify your account to start using Feelit'.format(user.username)
        from_email = 'Feelit <noreply@feelit.com>'
        content = render_to_string(
            'emails/users/account_verification.html',
            {
                'token': verification_token,
                'user': user
            }
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token(self, user):
        """ Create JWT token that the user can use to verify 
        its account.

        Time must be in UTC format for 'exp'
        """
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        # decode for decoding token in byte format
        return token.decode()


class UserLoginSerializer(serializers.Serializer):
    """ User login serializer."""

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """ Validate credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid Credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet')
        self.context['user'] = user
        return data

    def create(self, data):
        """ Generate new token."""

        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class AccountVerificationSerializer(serializers.Serializer):
    """ Account verification serializer. """

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify if token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid Token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid Token')

        self.context['payload'] = payload
        return data

    def save(self):
        """ Update user's verified status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()
