from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    username = models.CharField(max_length=100)
    USERNAME_FIELD = 'username'
    instagram_id = models.CharField(max_length=100, unique=True)
    is_professional = models.BooleanField(default=False)
