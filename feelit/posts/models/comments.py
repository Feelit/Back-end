"""Comments model."""

# Django
from django.db import models

# Utilities
from feelit.utils.models import FeelitModel


class Comment(FeelitModel):
    """ Comment model.

    Comments created by users inside other users post.
    The text in the comments would be rated by sentiment analysis.
    """

    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')

    from_user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        help_text='User that emits the comment',
        related_name='from_user'
    )
    for_user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        help_text='User that recives the comment',
        related_name='for_user'
    )
    text = models.TextField(blank=True)
    comment_rating = models.FloatField(null=True)

    def __str__(self):
        """ Return comment info."""
        return '@{} commented at @{}'.format(
            self.from_user,
            self.for_user
        )