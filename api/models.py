from django.contrib.auth.models import User
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    bio = models.CharField(max_length=100, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos', null=True, blank=True)

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    caption = models.TextField(max_length=300)

    def __str__(self):
        return f'{self.caption} created by {self.author.username}'


class Media(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_media')
    media_url = models.FileField(upload_to='media')

    def __str__(self):
        return f'{self.id} of post_id: {self.post.id}'


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    content = models.TextField(max_length=100);
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content} commented by {self.author.username}'


class Like(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')

    def __str__(self):
        return f'{self.author.username} likes post: {self.post}'
