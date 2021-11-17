from django.db import models

from .base import BaseModel
from .user import User


class Post(BaseModel):
    author = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, verbose_name="Author")
    title = models.CharField(max_length=500, null=False, blank=False, verbose_name="Title")
    body = models.TextField(max_length=5000, null=True, blank=True, verbose_name="Body")
    categories = models.ManyToManyField(
        "Category", db_table="post_category", verbose_name="Post categories", related_name="categories"
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "post"
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Name")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
