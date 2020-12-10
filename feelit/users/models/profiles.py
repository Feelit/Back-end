"""Profile model."""

# Django
from django.db import models

# Utilities
from feelit.utils.models import FeelitModel


class Profile(FeelitModel):
    """ Profile model.

    Profile holds user's public data like bio, posts and stats.
    """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    biography = models.TextField(max_length=250)
    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures',
        blank=True,
        null=True
    )

    # Stats
    profile_rating = models.FloatField(
        default=0.0,
        help_text="Feelings overall rating based on post results")

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)
