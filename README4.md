# [4주차 스터디] Serializer

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

## 4주차 과제

### 모델 선택 및 데이터 삽입

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

### 모든 데이터를 가져오는 API 만들기

- URL: `api/posts/`
- METHOD: `GET`
- 결과
```json
[
  {
    "id": 17,
    "author": "user1",
    "caption": "포스트111",
    "created_at": "2021-10-15T00:16:10.758938+09:00",
    "updated_at": "2021-10-15T00:16:10.758938+09:00",
    "comments": [
      {
        "author": "ming",
        "content": "Comment!!!!",
        "created_at": "2021-10-14T16:06:19.338Z"
      },
      {
        "author": "ceos",
        "content": "HI",
        "created_at": "2021-10-14T16:07:27.006Z"
      }
    ]
  },
  {
    "id": 18,
    "author": "user2",
    "caption": "포스트222",
    "created_at": "2021-10-15T00:16:17.708094+09:00",
    "updated_at": "2021-10-15T00:16:17.708094+09:00",
    "comments": [
      {
        "author": "user1",
        "content": "코멘트222",
        "created_at": "2021-10-14T16:06:31.398Z"
      }
    ]
  },
  {
    "id": 19,
    "author": "user3",
    "caption": "포스트333",
    "created_at": "2021-10-15T00:16:26.793209+09:00",
    "updated_at": "2021-10-15T00:16:26.793209+09:00",
    "comments": [
      
    ]
  }
]
```
