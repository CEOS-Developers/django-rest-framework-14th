from django.db import models
from base.models import Base
from user.models import User


class PostMedia(Base):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    MEDIA_TYPE_CHOICES = [
        ('VD', 'video'),
        ('IM', 'image')
    ]
    content_url = models.URLField()
    type = models.CharField(max_length=2, choices=MEDIA_TYPE_CHOICES)

    class Meta:
        db_table = 'post_media'


class PostLike(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_like')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='like')

    class Meta:
        db_table = 'post_like'


class PostTag(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tag_user')
    tagged_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tagged_user')

    class Meta:
        db_table = 'post_tag'


class Post(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    content_text = models.TextField(max_length=300)

    class Meta:
        db_table = 'post'

    def __str__(self):
        return self.content_text + ' created by ' + self.user.nickname

    def writer(self):
        # 이 게시물 쓴 사람
        return self.user.nickname + ' ' + self.when_created()

    def get_all_comments(self):
        # 이 게시물에 달린 댓글
        return self.comment.all()

    def get_likes(self):
        # 이 게시물에 달린 좋아요
        return PostLike.objects.filter(post__id=self.id).count()
