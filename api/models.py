from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BasedateModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True) # 최초 저장시에만 현재 날짜 적용.
    updated_date = models.DateTimeField(auto_now=True)  # save될 때마다 현재날짜로 갱신.

    class Meta:
        abstract = True

class User(AbstractUser):
    nickname = models.CharField(max_length=20,blank=False)
    gender_choice = (  # 성별 선택을 위한 필드.
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=2, choices=gender_choice)
    phone_num = models.IntegerField(blank=False)
    introduction = models.TextField(blank=True)
    website = models.URLField(max_length=50)
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

class Post(BasedateModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    title = models.TextField(blank=False)

    def __str__(self):
        return self.author.nickname + '_post_' + self.id

class Photo(BasedateModel):
    photo_url = models.ImageField(upload_to="post/Photos")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return 'photo_' + self.id

class Videos(BasedateModel):
    video_url = models.FileField(upload_to="post/Videos")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return 'video_' + self.id

class Comment(BasedateModel):
    comment = models.TextField(blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='post_comments')

    def __str__(self):
        return self.user.username + '_comments_post_' + str(self.post.id)

class Likes(BasedateModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')

    def __str__(self):
        return self.user.username + '_likes_post_' + str(self.post.id)

