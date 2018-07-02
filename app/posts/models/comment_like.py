from django.db import models
from members.models import User
from .comment import Comment


__all__ = (
    'CommentLike',
)


class CommentLike(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='commentlike_user',
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='in_comment'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} 님이 {self.comment}를 좋아합니다.'

    @property
    def username(self):
        return f'{self.user}'

    @property
    def comment_context(self):
        return f'{self.comment}'

