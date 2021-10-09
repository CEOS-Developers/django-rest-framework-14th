from time import timezone

from django.db import models

from api.models.user import User


class Story(models.Model):
    story_author = models.ForeignKey(User, on_delete=models.CASCADE)
    story_content = models.TextField()
    upload_time = models.DateTimeField(auto_now=True)

    def publish(self):
        self.upload_time = timezone.now()
        self.save()

    def __str__(self):
        return self.story_content
