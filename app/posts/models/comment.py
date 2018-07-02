from django.conf import settings
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
        related_name='comments',
    )

    _author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='comments',
        null=True,
        blank=True,
    )

    _content = models.TextField()

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self._author} : {self._content}'

    # def delete(self, *args, **kwargs):
    #     self.is_deleted = True
    #     self.save()

    @property
    def author(self):
        return self._author

    @property
    def content(self):
        if self.is_deleted:
            return '삭제된 댓글입니다.'
        return f'{self._content}'

    @property
    def post_context(self):
        return f'{self._content}'

    @property
    def username(self):
        return f'{self._author}'
