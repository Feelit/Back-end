""" Posts model."""

# Django
from django.db import models

# Utilities
from feelit.utils.models import FeelitModel


class Post(FeelitModel):
    """Post model."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='posts/photos', blank=True)
    post_rating = models.FloatField(null=True)

    def __str__(self):
        """Return title and username."""
        return '{} by @{}'.format(self.title, self.user.username)

