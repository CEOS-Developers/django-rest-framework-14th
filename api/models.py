from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True)
    private = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Post(BaseModel):
    text = models.TextField(blank=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return 'post_' + str(self.id)


class Image(BaseModel):
    image = models.ImageField(upload_to="images", null=True)
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return 'image_' + str(self.id)


class Video(BaseModel):
    video = models.FileField(upload_to="videos", null=True)
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return 'video_' + str(self.id)


class Like(BaseModel):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self):
        return self.user.username + '_likes_post' + str(self.post_id)


class Comment(BaseModel):
    text = models.CharField(max_length=100, blank=False)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='post_comments')

    def __str__(self):
        return self.user.username + '_comments_post' + str(self.post_id)
