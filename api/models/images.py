from django.db import models

from api.models.posts import Post


class Image(models.Model):
    post = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE)
    image_url = models.TextField()
