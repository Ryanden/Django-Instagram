from django.db import models
from members.models import User
from .post import Post


__all__ = (
    'PostLike',
)


class PostLike(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='postlike_username'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='postlike_postname'
    )

    liked_at = models.DateTimeField(auto_now_add=True)

    @property
    def post_name(self):
        return f'{self.post}'

    @property
    def username(self):
        return f'{self.user}'

