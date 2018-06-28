from django.db import models
from django.conf import settings

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
