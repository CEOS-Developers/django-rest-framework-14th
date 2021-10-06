from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True)
    bio = models.CharField(max_length=100, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos', null=True, blank=True)

    def __str__(self):
        return 'user: ' + self.username


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(max_length=300)

    def __str__(self):
        return 'post: ' + self.id + ', author: ' + self.author.username + ', at: ' + self.created_at


class Video(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video_url = models.FileField(upload_to='videos')

    def __str__(self):
        return 'video: ' + self.id + ', post: ' + self.post.id


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.FileField(upload_to='images')

    def __str__(self):
        return 'image: ' + self.id + ', post: ' + self.post.id


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(max_length=100);
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'comment: ' + self.content + ', author: ' + self.author.username


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username + ' likes ' + self.post.id
