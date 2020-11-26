"""Django models utilities."""

# Django
from django.db import models


class FeelitModel(models.Model):
    """Feelit base model.

    FeelitModel acts as an abstract base class from
    whic every other model will inherit. It provides
        + created (DateTime): Store the datetime the object was created.
        + modified (DateTime): Store the last datetime the object was modified.
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created'
    )

    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was last modified'
    )

    class Meta:
        """Meta class."""

        abstract = True

        # Latest by ascending 'created' date
        get_latest_by = 'created'
        ordering = ['-modified', '-created']