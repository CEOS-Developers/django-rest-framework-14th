from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    bio = models.CharField(max_length=100, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos', null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(max_length=300)

    def __str__(self):
        return f'{self.caption} created by {self.author.username}'


class Video(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video_url = models.FileField(upload_to='videos')

    def __str__(self):
        return f'{self.id} of post_id: {self.post.id}'


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.FileField(upload_to='images')

    def __str__(self):
        return f'{self.id} of post_id: {self.post.id}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=100);
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content} commented by {self.author.username}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username} likes post: {self.post}'
