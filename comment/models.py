from django.db import models
from base.models import Base
from user.models import User
from post.models import Post


class CommentLike(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_like', null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='like', null=True)

    class Meta:
        db_table = 'comment_like'


class CommentTag(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='comment_tag')

    class Meta:
        db_table = 'comment_tag'


class Comment(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    content_text = models.TextField(max_length=300)

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return self.user.nickname + ' says ' + self.content_text

    def get_likes(self):
        return CommentLike.objects.filter(comment__id=self.id).count()
