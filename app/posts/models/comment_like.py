from django.db import models
from members.models import User
from .comment import Comment


__all__ = (
    'CommentLike'
)


class CommentLike(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment_like',
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} 님이 {self.comment}를 좋아합니다.'
