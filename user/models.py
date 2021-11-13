from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from base.models import Base


class UserManager(BaseUserManager):
    def create_user(self, login_id, email, nickname, password, is_superuser=False):
        user = self.model(
            login_id=login_id,
            email=email,
            nickname=nickname,
            is_superuser=is_superuser
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, login_id, email=None, nickname=None, password=None, **extra_fields):
        superuser = self.create_user(
            login_id=login_id,
            nickname=nickname,
            password=password,
            email=email,
            is_superuser=True
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save()
        return superuser

    @staticmethod
    def follow(from_user, to_user):
        if from_user.is_following(to_user):
            raise ValueError

        relation = Follow(from_user=from_user, to_user=to_user)
        relation.save()


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    login_id = models.CharField(max_length=255, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=50, unique=True, null=False, blank=False)
    nickname = models.CharField(max_length=30, unique=True, null=False, blank=False)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='', blank=True)

    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['login_id', 'email']

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.nickname

    def get_all_posts(self):
        return self.post.all()

    def get_all_comments(self):
        return self.comment.all()

    def get_all_followers(self):
        return self.follower.all()

    def get_followers_count(self):
        return self.get_all_followers().count()

    def get_all_followings(self):
        return self.following.all()

    def get_followings_count(self):
        return self.get_all_followings().count()

    def is_following(self, to_user):
        try:
            self.following.get(to_user=to_user)

        except Follow.DoesNotExist:
            return False

        return True

    def is_followed(self, from_user):
        try:
            self.follower.get(from_user=from_user)

        except self.DoesNotExist:
            return False

        return True


class Follow(Base):
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follower')

    class Meta:
        db_table = 'follow'

    def __str__(self):
        return str(self.from_user.id) + ' follows ' + str(self.to_user.id)
