from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name="following"
    )


class Post(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    body = models.TextField(max_length=255)
    likes = models.ManyToManyField(User, blank=True, related_name="post_likes")
    timestamp = models.DateTimeField(auto_now_add=True)
