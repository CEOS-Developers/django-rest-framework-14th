from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone


class User(AbstractBaseUser):  # AbstractBaseUser를 상속받고 있는 모든 유저를 담은 모델
    username = models.CharField(max_length=255)  # 사용자의 이름 정의
    USERNAME_FIELD = 'username'
    insta_id = models.CharField(max_length=255, unique=True)  # 인스타 아이디
    email = models.EmailField(max_length=255, unique=True)
    tel = models.CharField("연락처", max_length=20, null=True, blank=True)


class Profile(models.Model):  # 유저의 세부 정보를 담는 모델
    owner = models.OneToOneField(User, on_delete=models.CASCADE)  # User모델과 1:1 로 관계
    nickname = models.CharField(max_length=40, blank=True)
    introduction = models.TextField(blank=True)  # 인스타 프로필 소개
    image = models.TextField()  # 인스타 사진
    # profile_name = models.TextField()  # 인스타에 표시한 이름


class Post(models.Model):  # 작성한 게시물을 담은 모델
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)  # 작성한 게시글
    location = models.TextField()  # 게시글 올린 장소
    create_date = models.DateTimeField(auto_now_add=True) # 게시글 올린 시간
    modify_date = models.DateTimeField(auto_now=True)
    goods = models.PositiveIntegerField()  # 좋아요 개수

    def publish(self): #?????
        self.upload_at = timezone.now()
        self.save()

    def __str__(self): #?????
        return self.content


class Image(models.Model):  # 해당하는 게시글
    post = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE)
    content = models.TextField()  # 이미지 url주소???


class Video(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

