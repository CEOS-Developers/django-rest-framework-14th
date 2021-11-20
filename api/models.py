from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password):

        if not email:
            raise ValueError('must have user email')
        if not password:
            raise ValueError('must have user password')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    objects = UserManager()

    username = models.CharField(max_length=255, unique=True)
    USERNAME_FIELD = 'username'
    instagram_id = models.CharField(max_length=255, unique=True)
    is_professional = models.BooleanField(default=False)

    class Meta:
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Profile(models.Model):
    profile_picture = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_name = models.TextField()
    profile_website = models.TextField()
    profile_info = models.TextField()


class Post(models.Model):
    post_author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    location = models.TextField()
    post_content = models.TextField()
    is_comment = models.BooleanField(default=True)
    upload_time = models.DateTimeField(auto_now=True)

    def publish(self):
        self.upload_time = timezone.now()
        self.save()

    def __str__(self):
        return self.post_content

    class Meta:
        managed = True
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')


class Image(models.Model):
    post = models.ForeignKey(Post, blank=False, null=False, on_delete=models.CASCADE)
    image_url = models.TextField()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment_post")
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    comment_content = models.TextField()
    upload_time = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Story(models.Model):
    story_author = models.ForeignKey(User, on_delete=models.CASCADE)
    story_content = models.TextField()
    upload_time = models.DateTimeField(auto_now=True)

    def publish(self):
        self.upload_time = timezone.now()
        self.save()

    def __str__(self):
        return self.story_content
