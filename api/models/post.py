from django.db import models
from .user import Profile


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content_text = models.TextField(max_length=300)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post'


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    content_url = models.TextField()
    playing_time = models.IntegerField()
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'video'


class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    content_url = models.TextField()
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'photo'


class PostLike(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post_like'


class PostTag(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post_tag'
