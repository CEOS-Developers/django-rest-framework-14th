from django.db import models

from api.models.user import User


class Profile(models.Model):
    profile_picture = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_name = models.TextField()
    profile_website = models.TextField()
    profile_info = models.TextField()
