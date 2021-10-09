from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return 'post_' + str(self.id)


class Image(models.Model):
    image = models.ImageField(upload_to="images", null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return 'image_' + str(self.id)


class Video(models.Model):
    video = models.FileField(upload_to="videos", null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return 'video_' + str(self.id)


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self):
        return self.user.username + '_likes_post' + str(self.post_id)


class Comment(models.Model):
    text = models.CharField(max_length=100, blank=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_comments')

    def __str__(self):
        return self.user.username + '_comments_post' + str(self.post_id)