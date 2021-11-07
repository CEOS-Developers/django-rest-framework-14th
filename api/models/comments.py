from django.db import models

from api.models.posts import Post
from api.models.user import User


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment_post")
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    comment_content = models.TextField()
    upload_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
