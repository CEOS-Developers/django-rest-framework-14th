from django.db import models

from api.models import User, Post


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')