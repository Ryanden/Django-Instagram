from ..models import Post
from rest_framework import serializers

__all__ = (
    'PostBaseSerializer',
)


class PostBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'photo',
            'content',
            'created_at',
            'like_users',
        )
