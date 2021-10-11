from django.db import models
from base.models import Base
from post.models import Post
from comment.models import Comment


class Hashtag(Base):
    content_text = models.TextField(max_length=300)

    class Meta:
        db_table = 'hashtag'


class HashtagPost(Base):
    hashtag = models.ForeignKey('Hashtag', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'hashtag_post'


class HashtagComment(Base):
    hashtag = models.ForeignKey('Hashtag', on_delete=models.CASCADE, related_name='comment_hashtag')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='hashtag')

    class Meta:
        db_table = 'hashtag_comment'
