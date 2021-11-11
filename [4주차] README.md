# DRF와 Serializer

## DRF란??

DRF(Django REST Framework)는 Django 내에서 RESTful API 설계를 돕는 라이브러리이다.

## Serializer란??

Serialize: 데이터를 문자열로 변환
Deserialize: 문자열을 데이터로 변환

Serializer는 쿼리셋, 모델 인스턴스 같은 복잡한 데이터를 python datatype으로 변환해준다. 이 데이터는 JSON, XML 등의 타입으로 쉽게 변환할 수 있다. 즉, Serializer는 데이터를 DRF에서 응답으로 사용할 수 있도록 JSON으로 표현해주는 역할을 한다. 반대로 deserializataion과 데이터 검증의 역할도 한다.

### Serializer 정의

Serializer를 정의하는 방법은 장고의 모델을 정의하는 것과 매우 유사하다.

- 예시 코드
```python
from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

### Serializer 사용

- 모델 인스턴스를 Python native datatype으로 변환하기
```python
comment = Comment(email='leila@example.com', content='foo bar')
serializer = CommentSerializer(comment)
serializer.data
# {'email': 'leila@example.com', 'content': 'foo bar', 'created': '2016-01-27T15:17:10.375877'}
```

- 최종적으로 JSON 형태로 변환하기
```python
from rest_framework.renderers import JSONRenderer

json = JSONRenderer().render(serializer.data)
json
# b'{"email":"leila@example.com","content":"foo bar","created":"2016-01-27T15:17:10.375877"}'
```

- python datatype을 다시 deserialize하기
```python
# data: JSON으로 받은 데이터를 python datatype(dictionary)으로 변환한 것
serializer = CommentSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# {'content': 'foo bar', 'email': 'leila@example.com', 'created': datetime.datetime(2012, 08, 22, 16, 20, 09, 822243)}
```

- deserialize한 데이터를 인스턴스로 저장하기
```python
def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance
```
serializer에 `creat()`와 `update()`를 정의하면, serializer instance에서 `save()`를 호출할 때 자동으로 두 메소드에 따라 데이터베이스에 object가 저장된다.
```python
# 새로운 인스턴스 저장
CommentSerializer(data=data).save()

# 인스턴스 업데이트 (comment: 이미 존재하는 인스턴스)
CommentSerializer(comment, data=data).save()
```

## ModelSerializer란??

ModelSerailizer를 사용하면 보다 쉽고 빠르게 모델에 대한 serializer를 만들 수 있다.

ModelSerializer 클래스와 Serializer 클래스의 차이점
- ModelSerializer는 자동으로 모델에 맞게 필드를 생성한다.
- ModelSerializer는 자동으로 validator를 생성한다.
- ModelSerializer는 기본적으로 `create()`와 `update()`가 구현되어 있다.

### Modelserializer 사용

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account	# 사용할 모델
        fields = ['id', 'account_name', 'users', 'created']	# 사용할 모델의 필드
```

## Serializer Relationship의 표현

1. ModelSerializer의 자동 생성

ModelSerializer는 `ForeignKey`를 `PrimaryKeyRelatedField`로 매핑한다.

2. Nested Serializer 사용

serializer를 필드처럼 사용해 relationship을 표현할 수 있다.

- 예시 코드
```python
class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['order', 'title', 'duration']

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

Nested serializer는 기본적으로 read-only이기 때문에 writable하게 하려면 `create()` 혹은 `update()`를 정의해야한다.

2. Serializer Method Field 사용

| SerializerMethodField(method_name=None)

`SerializerMethodField` 는 메소드를 호출하고 리턴 받은 값을 필드에 저장한다. `method_name`은 지정하지 않으면 `get_<field_name>`의 이름을 사용한다.

- 예시 코드
```python
class TrackSerializer(serializers.ModelSerializer):
    album_artist = serializers.SerializerMethodField()
		
		class Meta:
        model = Track
        fields = '__all__' 
		
    def get_album_artist(self, obj):  # obj: track 객체
        return obj.album.artist
```

---

# REST API 만들어보기

## 모델 선택 및 데이터 삽입

```python
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        

class Post(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    caption = models.TextField(max_length=300)

    def __str__(self):
        return f'{self.caption} created by {self.author.username}'


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    content = models.TextField(max_length=100);
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content} commented by {self.author.username}'
```
![Untitled (6)](https://user-images.githubusercontent.com/71026706/137359495-452bf067-ab1a-4a42-846c-24cfabbc83d4.png)
![Untitled (7)](https://user-images.githubusercontent.com/71026706/137359501-43cb5379-2949-47c6-a468-83e1f11a17cd.png)

post 모델을 선택해 api를 만들기로 해서 위와 같이 데이터를 3개 삽입하였다.

## Serializer 정의하기

```python
# serializers.py
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'caption', 'created_at', 'updated_at', 'comments']

    def get_author(self, obj):
        return obj.author.username

    def get_comments(self, obj):
        queries = obj.post_comments.all()
        comments = []
        for query in queries:
            comment = {'author': query.author.username, 'content': query.content, 'created_at': query.created_at}
            comments.append(comment)
        return comments
``` 

Post 모델의 Serializer를 정의하였다. 

그런데 현재 `get_comments()` 에서 **N+1 problem**이 발생하기 때문에 쿼리를 줄이는 것이 필요하다.

> 💡 **N+1 Problem이란??**
> <br>쿼리 1번으로 N건을 가져왔는데, 또다시 각 column을 얻기 위해 N번의 쿼리를 추가 수행하게 되는 문제를 N+1 (query) problem이라고 한다.

`obj.post_comments.all()`에서 1번 쿼리가 수행되고, `queries`(가져온 comments)의 `query.author.username`을 가져올 때 N번의 쿼리가 추가 수행된다.

### 쿼리 줄이기

1. `select_related` 사용하기

select하려는 모델이 single object인 경우, 즉 forward/backward OneToOne, forward ForeignKey일 때 사용한다. 1번의 쿼리로 관계된 모델들까지 가져올 수 있다.

1. `prefetch_related` 사용하기

select하려는 모델이 multiple object인 경우, 즉 forward/backward ManyToMany, backward ForeignKey일 때 사용한다. `prefetch_related` 는 각 모델에 대해 1번씩 쿼리를 수행한다.

```python
def get_comments(self, obj):
		queries = obj.post_comments.all().select_related('author')
    comments = []
    for query in queries:
        comment = {'author': query.author.username, 'content': query.content, 'created_at': query.created_at}
        comments.append(comment)
    return comments
```

Comment 모델이 User(author)를 정참조하기 때문에 `select_related` 를 사용해 seriealizer를 수정하였다.

## View와 URL

```python
# views.py
from .models import Post
from .serializers import PostSerializer
from rest_framework import viewsets

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # create() 재정의
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

```python
# urls.py
from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls))
]
```

## Authentication과 Permission

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # HTTP header로 사용자 id를 넘김 (테스트용으로만 사용)
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 인증된 요청만 허용 (로그인한 후에만 request 가능)
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

## API 테스트

- URL: `api/posts/`
- METHOD: `GET`
- 결과
    
    ![get](https://user-images.githubusercontent.com/71026706/140635420-df52f849-9e69-4905-9dd7-6051effbea72.png)
    
- URL: `api/posts/`
- METHOD: `POST`
- 결과
    
    ![post](https://user-images.githubusercontent.com/71026706/140635423-ec487865-647f-4fc8-a7bb-e210466f2086.png)
