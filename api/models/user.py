from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    USERNAME_FIELD = 'username'
    instagram_id = models.CharField(max_length=100, unique=True)
    is_professional = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'

