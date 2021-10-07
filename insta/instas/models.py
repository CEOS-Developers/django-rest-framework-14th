from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20, primary_key=True)
    user_pw = models.CharField(max_length=20)
    email =  models.EmailField()
    def __str__(self):
        return self.uid

class Profile(models.Model):
    uid = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20)
    website = models.CharField(max_length=40)
    introduction = models.TextField()
    phone_num = models.IntegerField()
    gender = models.CharField(max_length=6)
    followers = models.IntegerField()
    following = models.IntegerField()

    def __str__(self):
        return self.user_name

class Posts(models.Model):
    uid = models.ForeignKey(Users,on_delete=models.CASCADE)
    post_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20)
    location = models.CharField(max_length=30)
    title = models.TextField()
    email = models.EmailField()
    comments = models.TextField()
    likes = models.IntegerField()

    def __str__(self):
        return self.title

class Photos(models.Model):
    photo_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    photo_url = models.ImageField(upload_to="post/Photos")
    date = models.DateTimeField()

    def __str__(self):
        return self.photo_id

class Videos(models.Model):
    video_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    video_url = models.FileField(upload_to="post/Videos")
    date = models.DateTimeField()

    def __str__(self):
        return self.video_id

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(Users,on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment

class Story(models.Model):
    uid = models.ForeignKey(Users,on_delete=models.CASCADE)
    story_id = models.AutoField(primary_key=True)
    date = models.DateTimeField()

    def __str__(self):
        return self.story_id

