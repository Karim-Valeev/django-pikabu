from main.models import Comment
from main.models import Post
from rest_framework import serializers

from .user import UserSerializer


class PostForCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id"]


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    post = PostForCommentSerializer()
    # todo in_reply_to там только комменты, которые уже за постом закреплены

    class Meta:
        model = Comment
        fields = ("id", "author", "post", "created_at", "text")


# class CommentCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ("title", "body", "categories")
#
#
# class CommentUpdateSerializer(serializers.ModelSerializer):
#     author = UserSerializer()
#
#     class Meta:
#         model = Comment
#         fields = ("id", "created_at", "author", "title", "body", "categories")
#         read_only_fields = ("id", "created_at", "author")
