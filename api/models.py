from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone


class User(AbstractBaseUser):  # AbstractBaseUser를 상속받고 있는 모든 유저를 담은 모델
    username = models.CharField(max_length=255)  # 사용자의 이름 정의
    USERNAME_FIELD = 'username'
    insta_id = models.CharField(max_length=255, unique=True)  # 인스타 아이디
    email = models.EmailField(max_length=255, unique=True)
    tel = models.CharField("연락처", max_length=20, null=True, blank=True)



