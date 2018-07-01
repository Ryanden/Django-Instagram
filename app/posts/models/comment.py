from django.db import models
from members.models import User
from .post import Post


__all__ = (
    'Comment',
)


class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user'
    )

    content = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} : {self.content}'

    @property
    def post_context(self):
        return f'{self.content}'

    @property
    def username(self):
        return f'{self.user}'
