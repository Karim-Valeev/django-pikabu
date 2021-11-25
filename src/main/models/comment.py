from django.conf import settings
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

    @property
    def is_replying_allowed(self):
        if self.in_reply_to is not None:
            count = 1
            parent = Comment.objects.get(pk=self.in_reply_to.pk)
            while parent.in_reply_to is not None:
                count += 1
                # по сути можно сделать сложный возможно(но скорее всего нет) более оптимальный запрос
                parent = Comment.objects.get(pk=parent.in_reply_to.pk)
            return count <= int(settings.MAXIMUM_COMMENTS_NESTING)
        else:
            return True

    class Meta:
        db_table = "comment"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
