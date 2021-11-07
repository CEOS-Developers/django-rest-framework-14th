from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profile_img", null=True)

    def __str__(self):
        return self.user.username


class Post(BaseModel):
    text = models.TextField(blank=True)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return 'post_' + str(self.id) + ' / by_' + str(self.user.user.username) + ' / ' + str(self.text)


class Image(BaseModel):
    image = models.ImageField(upload_to="images", null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return 'image_' + str(self.image)


class Video(BaseModel):
    video = models.FileField(upload_to="videos", null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return 'video_' + str(self.video)


class Like(BaseModel):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self):
        return self.user.user.username + '_likes_post' + str(self.post.id)


class Comment(BaseModel):
    text = models.TextField(max_length=100, blank=False)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_comments')

    def __str__(self):
        return self.user.user.username + '_comments_post' + str(self.post.id)
