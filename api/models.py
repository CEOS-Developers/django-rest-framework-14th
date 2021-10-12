from django.contrib.auth.models import User
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=40, unique=True)
    introduction = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="image")

    def __str__(self):
        return self.nickname


class Post(BaseModel):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class File(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.FileField(upload_to="file")


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    writer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(blank=False)

    def __str__(self):
        return '{} commented {} post'.format(self.writer, self.post.author)

class Follow(BaseModel):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return '{} -> {}'.format(self.follower.nickname, self.following.nickname)

class Like(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return '{} liked post'.format(self.user.nickname)


