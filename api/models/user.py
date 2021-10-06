from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.TextField(max_length=15)

    class Meta:
        db_table = 'user'
