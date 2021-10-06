from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.TextField(max_length=15)
    private = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.nickname
