from members.serializer import UserSerializer
from ..models import Post
from rest_framework import serializers

__all__ = (
    'PostBaseSerializer',
)


class PostBaseSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)

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

        read_only_fields = (
            'author',
        )
