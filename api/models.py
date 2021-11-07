from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    bio = models.TextField(max_length=150, blank=True)
    profile_photo = models.ImageField(blank=True, upload_to='profiles', default='profiles/tmp4et5jeut.jpg')

    def clean(self):
        if not self.phone.isdigit():
            return ValidationError(_('Phone must be numeric only.'))

    def __str__(self):
        return self.account_name


class Post(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(max_length=2200, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.account_name}'s post: {self.caption}"


class Photo(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='photos')
    image_file = models.ImageField(upload_to='posts/photos')

    def __str__(self):
        return f"Photo from {self.post.profile.account_name} 's post: {self.post.caption}"


class Video(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='posts/videos', validators=[
        FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])
    ])

    def __str__(self):
        return f"Video from {self.post.profile.account_name} 's post: {self.post.caption}"


class Like(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return self.profile.account_name + ' liked ' + self.post.profile.account_name + "'s post: " + self.post.description


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=2200, blank=False)

    def __str__(self):
        return f"{self.profile.account_name}'s comment on {self.post.profile.account_name}'s post: {self.content}"


class FollowRelation(models.Model):
    follower = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='follow')
    followee = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='followed')

    def __str__(self):
        return f'{self.follower.account_name} follows {self.followee.account_name}'


Profile.add_to_class('followings', models.ManyToManyField('self', through=FollowRelation, related_name='followers', symmetrical=False))
