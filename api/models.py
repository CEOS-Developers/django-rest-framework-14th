from django.db import models
from django.contrib.auth.models import User
# from django.core.validators import FileExtensionValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_name = models.TextField(max_length=30)
    phone = models.TextField(max_length=20)
    bio = models.TextField(max_length=150)
    # profile_photo = models.ImageField(blank=True, upload_to='profiles')

    def __str__(self):
        return self.account_name


class Post(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='posts')
    description = models.CharField(max_length=255, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profile.account_name + "'s post: " + self.description


class Photo(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='photos')
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='photos')
    # image_file = models.ImageField(upload_to='posts/photos')

    def __str__(self):
        return 'Photo from ' + self.profile.account_name + ': ' + self.post.description


class Video(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='videos')
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='videos')
    # video_file = models.FileField(upload_to='posts/videos', validators=[
    #     FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])
    # ])

    def __str__(self):
        return 'Video from ' + self.profile.account_name + "'s post" + self.post.description


class Like(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return self.profile.account_name + ' liked ' + self.post.profile.account_name + "'s post: " + self.post.description


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.profile + ' left a comment on ' + self.post.profile.account_name + "'s post: " + self.post.description
