from django.db import models
from .profile import Profile


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content_text = models.TextField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post'

    def __str__(self):
        return self.user.nickname + '의 게시물 :: ' + self.content_text

    def when_created(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M:%S')

    def when_updated(self):
        return self.update_date.strftime('%Y-%m-%d %H:%M:%S')


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content_url = models.TextField(max_length=300)
    playing_time = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'video'

    def __str__(self):
        return self.content_url

    def when_created(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M:%S')


class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content_url = models.TextField(max_length=300)
    comment_block = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'photo'

    def __str__(self):
        return self.content_url

    def when_created(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M:%S')
