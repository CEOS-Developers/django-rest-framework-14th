from django.db import models
from .profile import Profile
from .comment import Comment
from .post import Post


class LikeComment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'like_comment'

    def when_created(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M:%S')


class LikePost(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'like_post'

    def when_created(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M:%S')
