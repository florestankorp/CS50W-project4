from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following"
    )


class Like(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class Post(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=63)
    body = models.TextField(max_length=255)
    likes = models.ManyToManyField(User, blank=True, related_name="post_likes")
    timestamp = models.DateTimeField(auto_now_add=True)
