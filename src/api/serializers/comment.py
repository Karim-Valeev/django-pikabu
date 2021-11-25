from main.models import Comment
from rest_framework import serializers


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    response_comments = RecursiveField(many=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "post", "in_reply_to", "created_at", "text", "response_comments")


class CommentCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = Comment
        fields = ("post", "in_reply_to", "text")


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "created_at", "author", "post", "in_reply_to", "text")
        read_only_fields = ("id", "created_at", "author", "post", "in_reply_to")
