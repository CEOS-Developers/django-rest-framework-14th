from django.db import models
from django.contrib.auth.models import User
from .member import Member
from .post import Post


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content_text = models.TextField(max_length=300)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comment'


class CommentLike(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comment_like';


class CommentTag(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comment_tag'
