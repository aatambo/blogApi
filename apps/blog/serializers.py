from rest_framework import serializers

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    """creates a serializer for posts"""

    author = serializers.ReadOnlyField(source="author.username")
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "body",
            "created",
            "comments",
        ]


class CommentSerializer(serializers.ModelSerializer):
    """creates a serializer for comments"""

    author = serializers.ReadOnlyField(source="author.username")
    post = serializers.ReadOnlyField(source="post.id")

    class Meta:
        model = Comment
        fields = ["id", "author", "post", "body", "created"]
