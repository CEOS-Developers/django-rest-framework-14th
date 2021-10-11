from django.db import models
from base.models import Base
from user.models import User


class Post(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_text = models.TextField(max_length=300)

    class Meta:
        db_table = 'post'

    def __str__(self):
        return self.content_text + ' created by ' + self.user.nickname

    def writer(self):
        return self.user.nickname + ' ' + self.when_created()

    def comments(self):
        # 이거 고쳐야되나 ?
        # 이 게시물에 달린 댓글 전부 출력
        return self.comment


class PostMedia(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    MEDIA_TYPE_CHOICES = [
        ('VD', 'video'),
        ('IM', 'image')
    ]
    content_url = models.URLField()
    type = models.CharField(max_length=2, choices=MEDIA_TYPE_CHOICES)

    class Meta:
        db_table = 'post_media'


class PostLike(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')

    class Meta:
        db_table = 'post_like'


class PostTag(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tag_user')
    tagged_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tagged_user')

    class Meta:
        db_table = 'post_tag'
