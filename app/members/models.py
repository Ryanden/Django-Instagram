from django.db import models

# Create your models here.


class InstagramUser (models.Model):

    name = models.CharField(max_length=50)


class UserInfo (models.Model):

    user = models.ForeignKey(
        InstagramUser,
        on_delete=models.CASCADE,
    )

