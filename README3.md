## 1. 인스타그램 모델 최종 수정 + ORM + DB 확인

인스타그램 모델 최종 수정본은 다음과 같습니다.

### 변경사항
* 기본 모델인 Base를 선언하여, 다른 모델에서 이를 기본으로 상속받아서 이용하게 하였다.   
* Follow모델의 manytomany관계에서, 중개 모델인 FollowRelation을 따로 설정하여 만들어주었다.

```angular2html
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


# 기본 Base 모델
class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) # 최초 작성 시간
    updated_at = models.DateTimeField(auto_now=True) # 최종 수정 시간

    class Meta:
        abstract = True


# 프로필 모델 구현
class Profile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # user model의 username(이름), password(비밀번호) 이용
    photo = models.ImageField(upload_to = "profile", blank=True) # 프로필 사진
    # 이용할 것-> username(이름), password(비밀번호)
    nickname = models.CharField(primary_key=True, max_length=20, unique=True) # 사용자 이름(인스타 아이디명) ex) ssssujini99 # unique=True 중복허용x
    website = models.URLField(blank=True) # 웹사이트
    intro = models.CharField(max_length=100, blank=True) # 소개
    email = models.EmailField(max_length=30, blank=True) # 이메일
    phone_num = PhoneNumberField(blank=True)
    GENDER_C = (
        ('여성', '여성'),
        ('남성', '남성'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_C) # 성별

    def __str__(self):
        return self.nickname  # 사용자 이름(인스타 아이디명)을 대표로 함


# 게시글 모델 구현
class Post(Base):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE) # 글쓴이 ## Profile - Post : One to Many 관계
    content = models.CharField(max_length=300, help_text="최대 길이 300자 입력이 가능합니다.", blank=True) # 내용


# (게시글에 업로드 할) 파일 모델 구현 <- 사진과 영상
class File(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 해당 게시글
    file = models.FileField(upload_to="post", blank=True) # 업로드 할 파일
    # url = models.CharField(max_length=300, blank=True)


# 좋아요 모델 구현
class Like(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 해당 게시글 ## Post - Like : One to Many 관계
    user = models.ForeignKey(Profile, on_delete=models.CASCADE) # 좋아요를 누른 사용자 ## Profile - Like : One to Many 관계


# 댓글 모델 구현
class Comment(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 해당 게시글 ## Post - Comment : One to Many 관계
    author = models.ForeignKey(Profile, on_delete=models.CASCADE) # 댓글을 쓴 사용자 ## Profile - Comment : One to Many 관계
    content = models.CharField(max_length=50) # 댓글 내용


# 북마크 모델 구현
class Bookmark(Base):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 해당 게시글
    user = models.ForeignKey(Profile, on_delete=models.CASCADE) # 북마크 한 사용자


# 팔로우 모델 구현
class Follow(Base):
    follower = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='follower', primary_key=True)
    followee = models.ManyToManyField(Profile, related_name='followee', through='FollowRelation') # follower가 팔로잉하는 사람들

    def __str__(self):
        return self.follower.nickname


# 팔로우-팔로잉 중개 모델 설정
class FollowRelation(Base):
    user = models.ForeignKey(Follow, on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.follower.nickname
```

* Follow모델과 FollowRelation이 db에 어떻게 되어있는지 shell창을 이용하여 확인해보겠습니다.   

![이미지](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FrlRhh%2FbtrhGbXHkln%2FMvswdhzDzpxSXVVhktR0F0%2Fimg.png)

* 이렇게 되어있는 것을 확인해볼 수 있습니다!

</br>

* 다음은, Pycharm의 로컬 터미널에서 이용자(Profile)을 추가하고,   
  팔로우-팔로잉 관계를 맺어보겠습니다.   


* 먼저 이용자는 sujin, user_1, user_2, user_3 이고요.   
  이를 추가하면 다음과 같습니다.


```angular2html
>>> from insta.models import Profile, Follow, FollowRelation
>>> from django.contrib.auth.models import User
>>>
>>> user_1 = User(username="user_1")
>>> user_1.save()
>>> profile_1 = Profile(user=user_1, nickname="user_1")
>>> profile_1.save()
>>>
>>> user_2 = User(username="user_2")
>>> user_2.save()
>>> profile_2 = Profile(user=user_2, nickname="user_2")
>>> profile_2.save()
>>>
>>> user_3 = User(username="user_3")
>>> user_3.save()
>>> profile_3 = Profile(user=user_3, nickname="user_3")
>>> profile_3.save()
>>>
>>> User.objects.all()
<QuerySet [<User: sujin>, <User: user_1>, <User: user_2>, <User: user_3>]>
>>> Profile.objects.all()
<QuerySet [<Profile: sujin>, <Profile: user_1>, <Profile: user_2>, <Profile: user_3>]>
>>>
```


* 이용자 4명을 추가했습니다.
  (sujin은 createsuperuser을 이용하여 만든 superuser입니다)


* 이렇게 만든 데이터를 db에서 확인하면 다음과 같습니다.   


![이미지](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbEkcWt%2FbtrhFQGh7tr%2FlOvyFuJKHJeklHbr7S0P51%2Fimg.png)


</br>


* 다음은 팔로우-팔로잉 관계입니다.   


* 팔로잉 관계는 다음과 같습니다
> sujin <-> user_1   
> sujin <-> user_2   
> sujin <-> user_3


먼저 이를 pycharm의 로컬 터미널에 추가해보겠습니다.


```angular2html
>>>
>>> sujin = Profile.objects.get(nickname="sujin")
>>> user_1 = Profile.objects.get(nickname="user_1")
>>> user_2 = Profile.objects.get(nickname="user_2")
>>> user_3 = Profile.objects.get(nickname="user_3")
>>>
>>>
# 먼저, sujin이 user_1, user_2, user_3을 팔로우합니다.
>>> sujin_f = Follow.objects.create(follower=sujin)
>>> sujin_f.followee.add(user_1)
>>> sujin_f.followee.add(user_2)
>>> sujin_f.followee.add(user_3)
>>>
# sujin이 팔로우하는 사람의 목록을 확인하면 다음과 같습니다.
>>> sujin_f.followee.all()
<QuerySet [<Profile: user_1>, <Profile: user_2>, <Profile: user_3>]>
>>> sujin_f.save()
>>>
>>>
# 다음으로, user_1이 sujin을 팔로우하겠습니다.
>>> user_1_f = Follow.objects.create(follower=user_1)
>>> user_1_f.followee.add(sujin)
>>> user_1_f.save()
>>>
>>> user_1_f.followee.all()
<QuerySet [<Profile: sujin>]>
>>>
# 다음으로, user_2가 sujin을 팔로우하겠습니다.
>>> user_2_f = Follow.objects.create(follower=user_2)
>>> user_2_f.followee.add(sujin)
>>> user_2_f.save()
>>>
>>> user_2_f.followee.all()
<QuerySet [<Profile: sujin>]>
>>>
# 다음으로, user_3이 sujin을 팔로우하겠습니다.
>>> user_3_f = Follow.objects.create(follower=user_3)
>>> user_3_f.followee.add(sujin)
>>> user_3_f.save()
>>>
>>> user_3_f.followee.all()
<QuerySet [<Profile: sujin>]>
>>>
```

</br>

> sujin <-> user_1   
> sujin <-> user_2   
> sujin <-> user_3   

위의 관계가 맺어졌습니다!   
그러면 이를 db에서 확인해보겠습니다.   

![이미지](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FopLkc%2FbtrhB2nAeof%2FocvmNnHchgjYZh4lt6dhuK%2Fimg.png)


insta_followrelation 테이블에서 보면,   
user_id는 해당 user이고,   
이 user가 팔로우한 사람이 following_id에 있는 것을 볼 수 있습니다!!   


또한, sujin.followee.all()을 통하여 sujin이 팔로우하는 사람들의 목록을    
모두 확인할 수 있음을 알 수 있습니다!   


django-admin 페이지에서 FollowRelation을 확인해봐도 잘 저장되어있음을 확인할 수 있습니다.   

![이미지](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fd2euM0%2FbtrhFylMKh4%2F0y5m2yqnLavVRV1G2mLlGk%2Fimg.png)



## 2. Django Rest Framework + Serializer


insta앱에 바로 DRF와 Serializer를 적용하기에 앞서   
연습이 필요할 것 같아 (insta앱의 모델들은 모델들의 관계가 복잡하다고 생각했기에) 

####이를 연습하고자 api앱을 만들고, 여기에 간단한 모델을 만들고   
####이를 modelSerializer를 이용하여 연습해보았습니다.
</br>

* 먼저 api앱의 models.py는 다음과 같습니다.

```angular2html
from django.db import models

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=200) # 제목
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
```

</br>

저는, 구현되어있는 모델을 이용할 것이므로 modelSerializer을 이용하였습니다.   

* api앱의 serializers.py
```angular2html
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
```



먼저, 관리자 페이지를 통해 저는 데이터 3개를 입력하였고,   
이 데이터들을 json으로 가져오면 다음과 같습니다.   

```angular2html
[
    {
        "id": 1,
        "title": "Set boiler plate app",
        "completed": false
    },
    {
        "id": 2,
        "title": "Configure urls and basic response222231",
        "completed": false
    },
    {
        "id": 3,
        "title": "Install DRF",
        "completed": false
    }
]
```
</br>


### ① 모든 데이터를 가져오는 api

* api/views.py
```angular2html
@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)
```

-> 즉, 모든 Task 데이터를 가져와서 이를 serializing한 데이터를 반환합니다.

* api/urls.py

```angular2html
path('task-list/', views.taskList, name='task-list'),
```

-> 위의 함수의 경로를 설정해주었습니다.   
루트는 api이므로 .../api/task-list 로 접속하면 이에 해당하는 view가 나타날 것입니다.   
이를 확인한 결과 다음과 같습니다.   

![이미지](https://postfiles.pstatic.net/MjAyMTEwMTRfMTU0/MDAxNjM0MTk3MDQ5Mzcw.ZqAOHdWKc54Cy3lOO7TNV_Dej9aBGAeR9DWvoPiLPtgg.Y21dwANjc1OvWgsfyyOEuZiQjpLDqgCHBrYaZAPbTcEg.PNG.sssssjin99/image.png?type=w966)

</br>

### ② 특정 데이터를 가져오는 api

* api/views.py
```angular2html
@api_view(['GET'])
def taskDetail(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)
```

-> 특정 pk에 해당하는 데이터만 가져와 이를 serializing한 데이터를 반환합니다.

* api/urls.py
```angular2html
path('task-detail/<int:pk>/', views.taskDetail, name='task-detail'),
```

-> pk=1에 해당하는 데이터를 가져와보겠습니다.

![이미지](https://postfiles.pstatic.net/MjAyMTEwMTRfMTE3/MDAxNjM0MTk3MDk3MDAz.rZ2vKifBvybjEZT16iANyrKoH-jiayCCGcLI8siQbHog.33zXDNiQvetRBszjab7STwdYEhyThezRIcx-nK12jvsg.PNG.sssssjin99/image.png?type=w966)



### ③ 데이터를 생성하는 api

* api/views.py
```angular2html
@api_view(['POST'])
def taskCreate(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
```

* api/urls.py
 ```angular2html
path('task-create/', views.taskCreate, name='task-crate'),
```

직접 데이터를 생성해보겠습니다.   

![이미지](https://postfiles.pstatic.net/MjAyMTEwMTRfMTI0/MDAxNjM0MTk3MTY0Njk4.D3XG7Rj9wCGJaPbll3sGKzd2zmiLbXDtmOprNrJkguUg.rW2PISMLuUWaf595K4hJtfIP2XXwlB1Z8MiM83B4s_cg.PNG.sssssjin99/image.png?type=w966)

이렇게 데이터를 추가하고, 추가한 결과 데이터가 생성되었음을 확인할 수 있습니다.    

![이미지](https://postfiles.pstatic.net/MjAyMTEwMTRfMTUw/MDAxNjM0MTk3MjU4MDk4.iohSUaXDfwU6_eVa5FWe0tLLvRfSOmu0Y8rOP0g5S8sg.ndrv1Kp6bTduQvxjqQjGHXSKOkP2Ech0vNRdK5m4EE4g.PNG.sssssjin99/image.png?type=w966)



### ④ 특정 데이터를 수정하는 api

* api/views.py
```angular2html
@api_view(['POST'])
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
```

-> 특정한 데이터를 pk로 받아서 해당 pk에 해당하는 데이터를 수정하고,   
   수정한 결과를 저장합니다.   

* api/urls.py
```angular2html
path('task-update/<int:pk>/', views.taskUpdate, name='task-update'),
```

pk=1에 해당하는 데이터를 수정해보고, 그 결과를 확인해보겠습니다.   
![이미지](https://postfiles.pstatic.net/MjAyMTEwMTRfMTk3/MDAxNjM0MTk3OTQ2OTk5.3b7MCkYTUuIdsknjurRRuFtFXJrV8SSwZHV11jgSl5Eg.oUzJkQoeYIi_SrrSQpDVqGpTOQSdJGgW64t2NxN2uNUg.PNG.sssssjin99/image.png?type=w966)
![이미지](https://postfiles.pstatic.net/MjAyMTEwMTRfMjg4/MDAxNjM0MTk3OTc4MDMx.WhJi9YJwjTLXj4YFOaTJU3J6fhiPkDbluBzXMV6sTzAg.gc_w4s7gAmd8V9smsC1BhkNGNKixwX28FrvOu3txJWwg.PNG.sssssjin99/image.png?type=w966)


잘 수정되었음을 확인할 수 있습니다

</br>


### ⑤ 특정 데이터를 삭제하는 api

* api/views.py
```angular2html
@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()

    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)

    return Response(serializer.data)
```

* api/urls.py
```angular2html
path('task-delete/<int:pk>/', views.taskDelete, name='task-delete'),
```

-> pk=9에 해당하는 데이터를 삭제하고 이를 확인해보겠습니다.   

![이미지](https://postfiles.pstatic.net/MjAyMTEwMTRfNTMg/MDAxNjM0MTk3MzAwODM0.tD3alKWl08kWV-A5RfyyCisbSjGSkSLOYs4h9wG7QIQg.EY51GUZc1ul6goYA1nhhXbALRRZA8Z0Lz-jzCYnaHgEg.PNG.sssssjin99/image.png?type=w966)
![이미지](https://postfiles.pstatic.net/MjAyMTEwMTRfMTAy/MDAxNjM0MTk3MzQyMzYw.dCGH0HtuX7SDGv50X-ysN4zd-BAdZHxWAnOR8ayd0Vgg.mjAiVgZRglplSZoDXAmpIKeEpcwKEMQovCe6NUyfPUgg.PNG.sssssjin99/image.png?type=w966)



 ## 정리
지금까지는, 다른 모델과 연관이 없는 단일 모델 하나에 대한 modelSerializer를 이용하였습니다.   

이후에 연관있는 모델에서는 어떻게 serializer를 이용하는지 공부한 이후,   
이를 insta앱에 적용해보도록 하겠습니다!




 # 4주차 과제 변경사항 + 추가

 ## insta 앱의 serializer 만들기

이번에는 저의 insta 모델에 대한 modelSerializer를 직접 만들어보았습니다!   
소개하면 다음과 같습니다.

```python
from rest_framework import serializers
from .models import Profile, Post, Comment, Follow, FollowRelation
from django.contrib.auth.models import User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField() # serializer method field 이용

    def get_author(self, obj):
        return obj.author.nickname # author의 값이 foreignkey로 pk인 id 값을 가져오기 때문에 nickname을 가져오도록 재정의

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'post']  # 정참조 시에는 그대로(author, post)


class PostListSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True) # Nested Serializer를 이용해 relation을 맺은 다른 모델과의 관계 표현하기
    author = serializers.SerializerMethodField() # serializer method field 이용

    def get_author(self, obj): # author의 값이 foreignkey로 pk인 id 값을 가져오기 때문에 nickname을 가져오도록 재정의
        return obj.author.nickname

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'comment_set']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'content']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class FolloweeListingField1(serializers.RelatedField):
    def to_representation(self, value):
        return value.follower.nickname


class ProfileListSerializer(serializers.ModelSerializer):
    post_set = PostListSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    followee = FolloweeListingField1(many=True, read_only=True) # many to many 관계 모델 기져오기

    class Meta:
        model = Profile
        fields = ['id', 'nickname', 'user', 'followee', 'post_set'] # followee: 역참조


class ProfilePartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'nickname', 'user']


class FolloweeListingField2(serializers.RelatedField):
    def to_representation(self, value):
        return value.nickname


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField()
    followee = FolloweeListingField2(many=True, read_only=True)

    def get_follower(self, obj):
        return obj.follower.nickname

    class Meta:
        model = Follow
        fields = ['follower', 'followee']
```


### serializers.py 를 만들면서 제가 느낀 점은 다음과 같습니다.   
1. foreignkey 관계의 모델을 serializer method field로 가져오고, 이를 get_<field_name>으로    
   pk값이 아닌 원하는 필드의 값으로 가져올 수 있어서 편리했다.   
2. nested serializer를 통해 serializer에서 상속과 같은 기능을 제공하는것을 알았고, 두 모델간의 관계를 표현할 때
   매우 유용하였다.

> 연관된 모델에서 가져와야 할 정보가 많은 경우 상속을 이용하는 nested serializer를 이용하고,   
> 연관된 모델에서 가져와야 할 정보가 한개정도로 작을 때, 그리고 원하는 필드 명으로 가져오고 싶을 때에는 serializer method field를 이용하면 될 것 같다   

3. 팔로우-팔로잉 관계를 어렵게 구현하여서, serializer로 이 관계를 가져올 때 많이 힘들었습니다.   
그래서 이 모델관계를 다시 수정하고 싶더라구요 ㅠㅠ   
> 모델관의 관계를 잘 짜야(단순하면서도 필요한 정보 명확히 표현할 수 있게) serializer의 구현이 편하다   

4. 한 모델에서 여러 개의 serializer를 구현할 필요가 있다.
> 생각을 해 보니, 한 모델에서 모든 정보가 다 필요한 경우가 있을 수 있고, 또는 특정 정보만이 필요할 수도 있습니다   
> 그래서 list, part 등으로 이름을 나눴는데 이름은 수정이 좀 더 필요할 것 같습니다.


 ## insta/urls.py

```python
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('profile/', views.profileList.as_view()), # 프로필 + (모든 정보를 가져오는) api
    path('profile/<int:pk>/', views.profileDetail.as_view()),
    # path('profiles/create/', views.profileCreate, name='profile-create'),
    #
    path('post/', views.postListAPIView.as_view()),
    path('post/<int:pk>/', views.postDetailAPIView.as_view()),
    #
    path('follow/', views.followList.as_view()),
    path('follow/<str:pk>/', views.followDetail.as_view()),
]
```

rest API를 공부해보고, 나름 restful하게 짜보려고 많이 노력해보았습니다!   
생각보다 url과 view의 함수명이 100% 마음에 들지는 않는 것 같았습니다   
직관적이면서도 간결하게? 그리고 중복되지 않게 표현하기가 나름 까다로운 것 같습니다

저는 처음에는 FBV를 기반으로 view 함수를 작성하였는데요,   
앞으로는 CBV기반으로 더 많이 쓴다고 하여서 한번 다 바꾸어보았습니다.   



## insta/views.py



```python
from django.shortcuts import render, redirect
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer, PostListSerializer, PostCreateSerializer, FollowSerializer, ProfileListSerializer, ProfilePartSerializer

from .models import Profile, Post, Follow
from django.contrib.auth.models import User

# 추가
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404


# Post 모델
# 1. 전체 Post 가져오기 or # 2. 새 Post 작성하기
class postListAPIView(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# 3. 특정 Post 가져오기 or # 4. 특정 포스트 수정하기 # 5. 특정 포스트 삭제하기
class postDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Post, id=pk)

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostListSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostCreateSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=201)


# Profile 모델
# 1. 전체 Profile 가져오기 or # 2. 새 Profile 작성하기 (보류)
class profileList(APIView):

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileListSerializer(profiles, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         내일 해보도록 하겠습니다.. 아무래도 abstractbase user model을 써야할 것 같습니다




# 3. 특정 Profile 가져오기 or # 4. 특정 Profile 수정하기 # 5. 특정 Profile 삭제하기
class profileDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Profile, id=pk)

    def get(self, request, pk, format=None):
        profile = Profile.objects.get(id=pk)
        serializer = ProfilePartSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        Profile = self.get_object(pk)
        serializer = ProfilePartSerializer(Profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        profile = self.get_object(pk)
        profile.delete()
        user = User.objects.get(id=pk)
        user.delete()
        return Response(status=204)


# # Follow 모델
# # 1. 전체 팔로우 관계 조회하기
class followList(APIView):
    def get(self, request, format=None):
        follows = Follow.objects.all()
        serializer = FollowSerializer(follows, many=True)
        return Response(serializer.data)


# # 2. 특정 유저의 팔로우 관계 조회하기
class followDetail(APIView):
    def get(self, request, pk, format=None):
        follow = Follow.objects.get(follower=pk)
        serializer = FollowSerializer(follow)
        return Response(serializer.data)
```


드디어 DRF를 이용하여 모든 http method를 구현해보았습니다.   
특정 url에 어떤 http method를 넣을지,   
url뒤에 파라미터까지 붙었을 때에는 또 어떤 method를 넣을지 고민을 하고 한 번 짜 보았습니다.   

이제 한번 직접 확인해보겠습니다!   
먼저, 정말 장고가 편리하다고 느낀 점 중 하나가 바로 장고의 rest framework 입니다.   
너무너무 유용한 것 같습니다.    

###ⓐ 먼저 'profile/' (모든 정보를 다 가져오는 api) 입니다.

![이미지]()