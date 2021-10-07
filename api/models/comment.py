from django.db import models
from .profile import Profile
from .post import Post


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content_text = models.TextField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return self.user.nickname + ' says ' + self.content_text

    def when_created(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M:%S')

    def when_updated(self):
        return self.update_date.strftime('%Y-%m-%d %H:%M:%S')
