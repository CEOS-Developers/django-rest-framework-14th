from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20, primary_key=True)
    user_pw = models.CharField(max_length=20)
    email =  models.EmailField()

class Profile(models.Model):
    uid = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20)
    website = models.CharField(max_length=40)
    introduction = models.TextField()
    phone_num = models.IntegerField()
    gender = models.CharField(max_length=6)
    post_id = models.IntegerField()
    followers = models.IntegerField()
    following = models.IntegerField()
    story_id = models.IntegerField()

class Posts(models.Model):
    uid = models.ForeignKey(Users,on_delete=models.CASCADE)
    post_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20)
    location = models.CharField(max_length=30)
    email = models.EmailField()
    comments = models.TextField()
    likes = models.IntegerField()
    files_id = models.IntegerField()

class Photos(models.Model):
    photo_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    photo_url = models.FileField()
    date = models.DateTimeField()

class Videos(models.Model):
    video_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    video_url = models.FileField()
    date = models.DateTimeField()

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(Users,on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment = models.TextField()

class Story(models.Model):
    uid = models.ForeignKey(Users,on_delete=models.CASCADE)
    story_id = models.AutoField()
    date = models.DateTimeField()

