from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, nickname, password, **extra_fields): # 일반 user 생성
        # 로그인 시 username이 아닌 nickname을 이용.
        if not nickname:
            raise ValueError("Users must have user nickname")
        user = self.model(
            nickname=self.normalize_nickname(nickname),
            password=password,
        )
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_admin', False)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password, **extra_fields): # 관리자 user 생성
        user = self.create_user(
            nickname=self.normalize_email(nickname),
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    objects = UserManager()

    nickname = models.CharField(max_length=50, null=False, unique=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    is_professional = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    email = models.EmailField(null=True, unique=True)
    phone_num = models.CharField(max_length=50, null=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # 사용자 username field를 nickname으로 설정하겠다.
    USERNAME_FIELD = 'nickname'
    # 필수로 작성해야하는 field. 항상 표시되기 때문에 USERNAME_FIELD나 비밀번호를 포함하면 안된다고...
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.nickname

    def get_real_name(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')
    image = models.ImageField(upload_to='profile_img', null=True)
    info = models.TextField(max_length=150, blank=True)
    website = models.TextField(max_length=150, blank=True)
    profile_name = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.nickname

    def get_real_name(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=500, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    comment_available = models.BooleanField(default=True)
    location = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return '{} : {}'.format(self.author.nickname, self.content)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}이 {}번째 글에 남긴 댓글 : {}'.format(self.author.nickname, self.post_id, self.content)


class File(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_files')
    file = models.FileField(upload_to='post_files')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self):
        return '{} likes {}'.format(self.user.nickname, self.post.content)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return '{} follows {}'.format(self.follower.nickname, self.following.nickname)