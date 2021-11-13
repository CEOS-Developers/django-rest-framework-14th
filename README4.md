## 변경사항1. 기존 User모델 1:1 연결 -> AbstractUser 모델 이용

```python
# 유저 모델 구현 -> AbstractUser이용
class User(AbstractUser, Base):
    photo = models.ImageField(upload_to = "profile", blank=True, null=True) # 프로필 사진
    website = models.URLField(blank=True, null=True) # 웹사이트
    intro = models.CharField(max_length=100, blank=True, null=True) # 소개
    phone_num = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return self.username  # 사용자 이름(인스타 아이디명)을 대표로 함
```

기존 auth user모델을 일대일 연결을 했을 경우,   
api로 유저를 post, put, delete할 때에, 기존의 user모델과 또한 이를 연결한 모델에 두 번 접근해야하므로   
이에 대해 불편함을 느꼈고, 이에 대한 해결방안으로 AbstractUser모델을 상속받기로 결정했다.   

이용은 매우 간단하다.   
AbstractUser를 상속함으로써, 이전의 유저모델 필드를 모두 상속하고,   
내가 따로 필요한 부분은 필드에 선언하였다.   

db에서 필드를 확인하면 다음과 같이 되어있는것을 볼 수 있다.   

![이미지](https://postfiles.pstatic.net/MjAyMTExMTFfNiAg/MDAxNjM2NjE1NTMzNDQ0.esZ-uJM3ZimAtGnlW4Q7monomdDePoM__sQKFSX3SgQg.uF2yRwg3J_xWtlxL3J0QpTEfMue-3kW5opRiPkIdx_Yg.PNG.sssssjin99/image.png?type=w966)


## 2. CBV 기반의 API View 작성

```python
from django.shortcuts import render, redirect
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer, UserCreateSerializer, PostListSerializer, PostCreateSerializer

from .models import User, Post

## 추가
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404


# Post 모델
# 1. 전체 Post 가져오기 or # 2. 새 Post 작성하기
class postList(APIView):
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
class postDetail(APIView):
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


# User 모델
# 1. 전체 User 가져오기 or # 2. 새 User 추가하기 (보류)
class userList(APIView):

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)




# 3. 특정 User 가져오기 or # 4. 특정 User 수정하기 # 5. 특정 User 삭제하기
class userDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(User, id=pk)

    def get(self, request, pk, format=None):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = User.objects.get(id=pk)
        user.delete()
        return Response(status=204)
```


### User모델에 대해서 HTTP 요청을 처리해보았습니다.

### 2-1) 모든 user list를 가져오는 API - 'insta/users/'

```json
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "username": "ssssujini99",
        "email": "sssssjin99@naver.com",
        "created_at": "2021-11-11T15:14:13.315412",
        "updated_at": "2021-11-11T15:14:13.315412"
    },
    {
        "id": 2,
        "username": "user2",
        "email": "user2@naver.com",
        "created_at": "2021-11-11T15:15:48.135898",
        "updated_at": "2021-11-11T15:15:48.135898"
    },
    {
        "id": 3,
        "username": "user3",
        "email": "user3@naver.com",
        "created_at": "2021-11-11T15:16:20.686877",
        "updated_at": "2021-11-11T15:16:20.686877"
    },
    {
        "id": 4,
        "username": "user4",
        "email": "user4@naver.com",
        "created_at": "2021-11-11T15:22:03.233465",
        "updated_at": "2021-11-11T15:22:03.233465"
    },
    {
        "id": 5,
        "username": "user5",
        "email": "user5@naver.com",
        "created_at": "2021-11-11T15:22:42.444570",
        "updated_at": "2021-11-11T15:22:42.444570"
    },
    {
        "id": 6,
        "username": "user6",
        "email": "user6@naver.com",
        "created_at": "2021-11-11T15:33:11.980960",
        "updated_at": "2021-11-11T15:33:11.980960"
    },
    {
        "id": 7,
        "username": "user7_edit",
        "email": "user7@naver.com",
        "created_at": "2021-11-11T15:40:31.556384",
        "updated_at": "2021-11-11T15:45:00.997762"
    }
]
```

### 2-2) 특정 user를 가져오는 API - 'insta/users/<int:pk>/'
ex) 'insta/users/1/'

```json
HTTP 200 OK
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "username": "ssssujini99",
    "email": "sssssjin99@naver.com",
    "created_at": "2021-11-11T15:14:13.315412",
    "updated_at": "2021-11-11T15:14:13.315412"
}
```


### 2-3) 새로운 user를 생성하는 API - 'insta/users/'

user8을 생성해보겠습니다.

![이미지](https://postfiles.pstatic.net/MjAyMTExMTFfNjEg/MDAxNjM2NjE1NTM4Nzgz.6todrZPg_5NC71dW1A_U8ZCEUdk9H3et8Qxc54F5MmMg.4HbTBmm5wR-t46HUcHFRrjJCLLwf1CXINonKiBuVlt4g.PNG.sssssjin99/image.png?type=w966)

생성하고 결과를 확인하면 다음과 같습니다.

![이미지](https://postfiles.pstatic.net/MjAyMTExMTFfMTc4/MDAxNjM2NjE1NTQzNTcw.PyMSPlzX6kPMcVKm8agfGbA7ciuYn57oVjFDnmfdoVog.hL6WuYzdBqPSAyoqXfYU0uYHRGnjaAvt0nzS7jP8JgUg.PNG.sssssjin99/image.png?type=w966)


### 2-4) 특정 user를 업데이트하는 API - 'insta/users/<int:pk>/'

ex) 'insta/users/8/'

user8을 업데이트 해보겠습니다. -> PUT 이용

![이미지](https://postfiles.pstatic.net/MjAyMTExMTFfMjY1/MDAxNjM2NjE1NTUwNDQ3.lGbRl8NuR15jnfDlyJYTINjx9nkeygigfY5_WfnukWYg.wo_pAVZkxtows15bWXaLv6gwH9MdIablQNkGBNBN6DIg.PNG.sssssjin99/image.png?type=w966)

수정하고 결과를 확인하면 다음과 같습니다.

![이미지](https://postfiles.pstatic.net/MjAyMTExMTFfMjk3/MDAxNjM2NjE1NTU0OTEz.YNyzp6iElyENI2qacEw0mWlEfgzthBvjk3hX_JdJGj4g.k6c-KIOCX2bd9RXMWhkbG-kH3RHAxnLtfAc4FNAd9L8g.PNG.sssssjin99/image.png?type=w966)



### 2-5) 특정 user를 삭제하는 API - 'insta/users/<int:pk>/'

ex) 'insta/users/8/'

user8을 삭제하고 결과를 확인해보겠습니다.

![이미지](https://postfiles.pstatic.net/MjAyMTExMTFfMjc0/MDAxNjM2NjE1NTYxMTcx.7HCUlXXV1_e8KMV1EV0MmFilG3VLCw_N7St9_iADyB8g.YP2I7WTv8z_TCza6h370562-yW45XNzAVnqD83xl7JQg.PNG.sssssjin99/image.png?type=w966)

삭제하고 결과를 확인하면 다음과 같습니다.

![이미지](https://postfiles.pstatic.net/MjAyMTExMTFfNDYg/MDAxNjM2NjE1NTY4Nzc2.Sp_-SfMSvO571z1aW6x_rt6HsYPMcaGXTW2rfGCX02kg.vFT7Z6kKuA_-ozMljZn_v7a7eBOXM2SuR4E91ucqK6Ug.PNG.sssssjin99/image.png?type=w966)

user8이 없어진 것을 확인할 수 있습니다.



## 공부한 내용 정리

## 간단한 회고