from django.db import models
from .profile import Profile


class Follow(models.Model):
    following_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    follower_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'follow'

    def when_created(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M:%S')
