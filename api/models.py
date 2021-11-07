from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

# Base model
class BaseModel(models.Model):
    # 삭제는 Boolean으로 관리하고 실제 DB에서는 지우지 않았다
    isDeleted = models.BooleanField(default=False)
    deletedAt = models.DateTimeField(null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        # abstract로 정의해 다른 모델이 상속 받을 수 있다
        # abstract = False라면 migrate시 DB에 테이블이 생성된다
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deletedAt = datetime.now()
        self.save()

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50, null=True, default=None)
    lastName = models.CharField(max_length=50, null=True, default=None)
    picture = models.CharField(max_length=200, null=True, default=None)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.username

class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=300)
    location = models.CharField(max_length=100)

    class Meta:
        db_table = 'post'

    def __str__(self):
        return 'post_' + str(self.id)

class File(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.CharField(max_length=300)

    class Meta:
        db_table = 'file'

    def __str__(self):
        return 'file_' + str(self.id)

class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return 'comment_' + str(self.id)

class Like(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'like'

    def __str__(self):
        return 'like_' + str(self.id)

class Follow(BaseModel):
    follower_user = models.ForeignKey(User, related_name='follower_user', on_delete=models.CASCADE)
    followee_user = models.ForeignKey(User, related_name='followee_user', on_delete=models.CASCADE)

    class Meta:
        db_table = 'follow'

    def __str__(self):
        return 'follow_' + str(self.id)