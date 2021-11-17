from django.db import models

from .base import BaseModel
from .post import Post
from .user import User


class Comment(BaseModel):
    author = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Author")
    text = models.TextField(max_length=3000, null=True, blank=True, verbose_name="Text")
    post = models.ForeignKey(
        Post, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Under post", related_name="comments"
    )
    in_reply_to = models.ForeignKey(
        "Comment",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="In reply to",
        related_name="response_comments",
    )
    # likes - M2M

    class Meta:
        db_table = "comment"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
