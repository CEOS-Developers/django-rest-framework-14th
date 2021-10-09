from time import timezone

from django.db import models

from api.models.user import User


class Post(models.Model):
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.TextField()
    numOfLike = models.PositiveIntegerField()
    post_content = models.TextField()
    is_comment = models.BooleanField()
    upload_time = models.DateTimeField(auto_now=True)

    def publish(self):
        self.upload_time = timezone.now()
        self.save()

    def __str__(self):
        return self.post_content
