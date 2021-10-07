from django.db import models
from .profile import Profile
from .comment import Comment
from .post import Post


class Hashtag(models.Model):
    id = models.AutoField(primary_key=True)
    hashtag = models.TextField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hashtag'

    def __str__(self):
        return self.hashtag

    def when_created(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M:%S')


class HashtagComment(models.Model):
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'hashtag_comment'


class HashtagPost(models.Model):
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'hashtag_post'
