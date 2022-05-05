import uuid

from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
     updating ``created`` and ``modified`` fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created"]


class Post(TimeStampedModel):
    """creates a model for posts"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    """creates a model for comments"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()

    def __str__(self):
        return f"{self.author} on {self.post}"
