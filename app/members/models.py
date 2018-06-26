from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):

    img_profile = models.ImageField(upload_to='user', blank=True)

    site = models.URLField(blank=True)

    introduction = models.TextField(blank=True)

    CHOICES_GENDER = (
        ('m', '남성'),
        ('f', '여성'),
        ('x', '선택안함'),
    )

    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)

    def __str__(self):
        return self.username
