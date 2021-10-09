from __future__ import unicode_literals
from django.db import models


# Create your models here.

class Users(models.Model):
    uid = models.IntegerField()
    user_name = models.CharField(max_length=20)
    user_id = models.CharField(max_length=20)
    website = models.CharField(max_length=40)
    introduction = models.CharField()
    email = models.EmailField()
    phone_num = models.IntegerField()
    gender = models.CharField(max_length=6)
    post_id = models.IntegerField()
    followers = models.IntegerField()
    following = models.IntegerField()
    story_id = models.IntegerField()

class Posts(models.Model):
    uid = models.ForeignKey(Users,on_delete=models.CASCADE)
    post_id = models.IntegerField()
    user_id = models.ForeignKey
