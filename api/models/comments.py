from django.db import models

from api.models.posts import Post
from api.models.user import User


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField()
    upload_time = models.DateTimeField(auto_now=True)
