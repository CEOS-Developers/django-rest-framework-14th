from django.db import models
from .user import Profile
from .comment import Comment
from .post import Post


class Hashtag(models.Model):
    id = models.AutoField(primary_key=True)
    hashtag = models.TextField(max_length=30)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hashtag'


class CommentHashtag(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment_hashtag'


class PostHashtag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'post_hashtag'
