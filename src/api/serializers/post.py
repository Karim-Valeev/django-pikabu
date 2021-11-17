from main.models import Category
from main.models import Post
from rest_framework import serializers

from .user import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    categories = CategorySerializer(many=True)

    class Meta:
        model = Post
        fields = ("id", "author", "title", "body", "categories", "created_at")


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "body", "categories")


class PostUpdateSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ("id", "created_at", "author", "title", "body", "categories")
        read_only_fields = ("id", "created_at", "author")
