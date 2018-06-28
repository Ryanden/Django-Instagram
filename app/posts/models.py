from django.db import models
from django.conf import settings
from members.models import User

# Create your models here.


class Post(models.Model):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    photo = models.ImageField(upload_to='post', blank=True)

    content = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.content


class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='my_comment',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_user'
    )

    content = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} : {self.content}'

