from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


# 기본 Base 모델
class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) # 최초 작성 시간
    updated_at = models.DateTimeField(auto_now=True) # 최종 수정 시간

    class Meta:
        abstract = True


# 유저 모델 구현 -> AbstractUser이용
class User(AbstractUser, Base):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    photo = models.ImageField(upload_to = "profile", blank=True, null=True) # 프로필 사진
    website = models.URLField(blank=True, null=True) # 웹사이트
    intro = models.CharField(max_length=100, blank=True, null=True) # 소개
    phone_num = PhoneNumberField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=30, blank=True, null=True) # 성별

    def __str__(self):
        return self.username  # 사용자 이름(인스타 아이디명)을 대표로 함


# 게시글 모델 구현
class Post(Base):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 글쓴이 ## User - Post : One to Many 관계
    content = models.CharField(max_length=300, help_text="최대 길이 300자 입력이 가능합니다.", blank=True) # 내용

    def __str__(self):
        return self.content # 포스트 내용을 대표로 함


# (게시글에 업로드 할) 파일 모델 구현 <- 사진과 영상
class File(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 해당 게시글
    file = models.FileField(upload_to="post") # 업로드 할 파일


# 좋아요 모델 구현
class Like(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 해당 게시글 ## Post - Like : One to Many 관계
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 좋아요를 누른 사용자 ## User - Like : One to Many 관계


# 댓글 모델 구현
class Comment(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 해당 게시글 ## Post - Comment : One to Many 관계
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 댓글을 쓴 사용자 ## User - Comment : One to Many 관계
    content = models.CharField(max_length=50) # 댓글 내용

    def __str__(self):
        return self.content # 댓글 내용을 대표로 함


# 북마크 모델 구현
class Bookmark(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 해당 게시글
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 북마크 한 사용자


# 팔로우 모델 구현
class Follow(Base):
    userFrom = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    userTo = models.ForeignKey(User, related_name='followee', on_delete=models.CASCADE)