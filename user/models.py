from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import Base


class User(AbstractUser, Base):
    nickname = models.TextField(max_length=15)
    bio = models.TextField(max_length=300)
    profile_picture = models.ImageField(upload_to='')

    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.nickname

    def get_all_posts(self):
        return self.post.all()

    def get_all_comments(self):
        return self.comment.all()

    def get_all_followers(self):
        return self.follower.all()

    def get_followers_count(self):
        return self.get_all_followers().count()

    def get_all_followings(self):
        return self.following.all()

    def get_followings_count(self):
        return self.get_all_followings().count()


class Follow(Base):
    following_user = models.ForeignKey('user', on_delete=models.CASCADE, related_name='following')
    follower_user = models.ForeignKey('user', on_delete=models.CASCADE, related_name='follower')

    class Meta:
        db_table = 'follow'

    def __str__(self):
        return self.following_user.nickname + ' follows ' + self.follower_user.nickname
