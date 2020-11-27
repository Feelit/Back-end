"""User model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser


# Utilities
from feelit.utils.models import FeelitModel


class User(FeelitModel, AbstractUser):
    """User model.

    Extend from Django's Abstract User and add extra fields.
    """

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'That email is already in use.'
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user have verified its email.'
    )


    def __str__(self):
        """Return username."""
        return self.username

    # overwrite the existing method
    def get_short_name(self):
        """ Return username."""
        return self.username
        