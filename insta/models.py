from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


# 프로필 모델 구현
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # user model의 username(이름), password(비밀번호) 이용
    photo = models.ImageField(upload_to = "profile", blank=True) # 프로필 사진
    # 이용할 것-> username(이름), password(비밀번호)
    nickname = models.CharField(max_length=20, unique=True) # 사용자 이름(인스타 아이디명) ex) ssssujini99
    website = models.URLField(blank=True) # 웹사이트
    intro = models.CharField(max_length=100, blank=True) # 소개
    email = models.EmailField(max_length=30, null=True) # 이메일
    phone_num = PhoneNumberField(blank=True)
    GENDER_C = (
        ('여성', '여성'),
        ('남성', '남성'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_C) # 성별

    def __str__(self):
        return self.nickname  # 사용자 이름(인스타 아이디명)을 대표로 함


# 게시글 모델 구현
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 글쓴이
    photo = models.ImageField(upload_to = "post") # 사진
    content = models.CharField(max_length=300, help_text="최대 길이 300자 입력이 가능합니다.") # 내용
    created_at = models.DateTimeField(auto_now_add = True) # 최초 작성 시간
    updated_at = models.DateTimeField(auto_now = True) # 최종 수정 시간

    # many-to-many 모델 연결시키기
    likes = models.ManyToManyField('Like', related_name='like_posts', blank=True)
    comments = models.ManyToManyField('Comment', related_name='comment_posts', blank=True)


# 좋아요 모델 구현
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


# 댓글 모델 구현
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


# 북마크 모델 구현
class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
