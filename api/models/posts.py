from time import timezone

from django.db import models

from api.models.user import User


class Post(models.Model):
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.TextField()
    post_content = models.TextField()
    is_comment = models.BooleanField(default=True)
    upload_time = models.DateTimeField(auto_now=True)

    def publish(self):
        self.upload_time = timezone.now()
        self.save()

    def __str__(self):
        return self.post_content

    class Meta:
        managed = True
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
