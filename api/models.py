from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    author = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    website = models.CharField(max_length=40)
    introduction = models.TextField(blank=True)
    phone_num = models.IntegerField(blank=False)
    gender = models.CharField(max_length=6)

    def __str__(self):
        return self.introduction

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    location = models.CharField(max_length=30)
    title = models.TextField(blank=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Photo(models.Model):
    photo_url = models.ImageField(upload_to="post/Photos")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.photo_url

class Videos(models.Model):
    video_url = models.FileField(upload_to="post/Videos")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_url

class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class Story(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author

class ViewUser(models.Model):
    author = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    story_id = models.ForeignKey(Story, on_delete=models.CASCADE)

class Likes(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author
