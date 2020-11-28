""" Posts model."""

# Django
from django.db import models

# Utilities
from feelit.utils.models import FeelitModel


class Post(FeelitModel):
    """Post model."""

    user = models.ForeignKey('users.User', on_delete=models.SET_NULL)
    profile = models.ForeignKey('users.Profile', on_delete=models.SET_NULL)

    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='posts/photos')
    post_rating = models.FloatField(default=5)

    def __str__(self):
        """Return title and username."""
        return '{} by @{}'.format(self.title, self.user.username)

