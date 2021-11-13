## 인스타그램 모델링

먼저, 인스타그램 어플에 접속하여 어떠한 항목들이 있는지 정리해보았다.

![스크린샷 2021-10-08 오전 2 12 23](https://user-images.githubusercontent.com/69099144/136434404-c4e72f78-249d-4d68-a12e-c59f9203f5ed.png)


모델링 사진

### User

유저를 식별하기 위해 어떤 값을 사용해야 할지 고민을 했는데, 인스타그램 아이디는 중복이 불가능하므로 아이디로만 식별이 가능하다고 생각했다. 다른 곳에서 외래 키로 이 값을 많이 사용할 것인데, uid 값을 따로 지정하는 것이 옳은지 고민을 계속 했는데 정답이 무엇인지 모르겠다.

그리고 비밀번호와 이메일 값만 저장해 놓게 만들었다.

```python
class Users(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)
    user_pw = models.CharField(max_length=20)
    email =  models.EmailField()
    def __str__(self):
        return self.user_id
```

### Profile

앞서 만든 유저모델의 아이디를 외래키로 받아오고, 그 값을 기본키로 사용하도록 하였다. 프로필과 유저는 한 몸이라는 생각이 들었다. 그래서 일대일 관계를 갖도록 하였다.

나머지 항목들은 프로필에 속하는 항목이니 설명을 생략한다.

```python
class Profile(models.Model):
    user_id = models.OneToOneField(Users,on_delete=models.CASCADE, primary_key=True)
    user_name = models.CharField(max_length=20)
    website = models.CharField(max_length=40)
    introduction = models.TextField()
    phone_num = models.IntegerField()
    gender = models.CharField(max_length=6)
    followers = models.IntegerField()
    following = models.IntegerField()

    def __str__(self):
        return self.user_name
```

### 게시물

게시물은 게시물 번호를 기본키로 갖고, 유저마다 게시글이 여러개가 존재할 수 있기 때문에 일대다 관계를 갖도록 하였다. 내용과 좋아요, 위치값도 갖는다.

```python
class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    location = models.CharField(max_length=30)
    title = models.TextField()
    likes = models.IntegerField()

    def __str__(self):
        return self.title
```

### 비디오, 사진

게시물 마다 비디오나 사진이 필수적이고, 여러개가 존재할 수 있기 때문에 다대일 관계를 갖는다. 그리고 개체들이 저장되는 링크도 설정해 주었다.

```python
class Photos(models.Model):
    photo_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    photo_url = models.ImageField(upload_to="post/Photos")
    date = models.DateTimeField()

    def __str__(self):
        return self.photo_id

class Videos(models.Model):
    video_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    video_url = models.FileField(upload_to="post/Videos")
    date = models.DateTimeField()

    def __str__(self):
        return self.video_id
```

### 댓글

```python
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment
```

댓글 또한 비디오, 사진과 성격이 비슷하다고 생각이 들었기 때문에 거의 비슷하다.

### 스토리

```python
class Story(models.Model):
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    story_id = models.AutoField(primary_key=True)
    date = models.DateTimeField()

    def __str__(self):
        return self.story_id
```

스토리라는 기능이 있는데, 이기능을 어떻게 데이터베이스에 집어넣을까 생각을 해보니 게시글과 비슷하게 짜보면 어떨까라는 생각이 들었다. 그런데, 이 스토리를 조회한 유저들의 정보를 저장해야 하는데, 이 부분은 모델링을 하지 못했다. 더 고민을 해봐야 할 것 같다.

## ORM 이용해보기

### 객체 생성

![스크린샷 2021-10-08 오전 2 10 56](https://user-images.githubusercontent.com/69099144/136434473-76bff5ac-193c-4b31-a6e0-30c4e7c3575b.png)


포스트 객체 생성하기

### 필터 적용해보기

![스크린샷 2021-10-08 오전 2 12 00](https://user-images.githubusercontent.com/69099144/136434487-4981c1d4-5fdd-4bf5-9ce8-bb0e6fb8f945.png)

필터

## 회고

장고를 처음 사용해보고, 모델링도 거의 처음해봤는데, 나름 만족스럽지만 하다보니 계속 고민되는 부분과 아쉬운 부분이 많았다. 피드백을 받는게 기대가 되며, 주말동안 더 수정을 해보려고 한다.
그리고 어떻게 구조가 짜여지는 지 어느정도 느낌이 오는 것 같다. 공부 많이 해야겠다.

# 주말동안 공부한 것

## 수정 모델

![스크린샷 2021-10-10 오전 12 48 28](https://user-images.githubusercontent.com/69099144/136685943-10590df7-b239-496c-8435-22df6cc9c2d2.png)


## 내가 느낀 것

1. 식별 / 비식별 관계 차이 확실히 짚어보자. 모델링 할 때 굉장히 중요하다.
2. id는 내가 정의해주지 않더라도 디비에 추가할 때 알아서 생긴다. 공부해보기
3. 논리 / 물리도 구분해보자.
4. 유저 모델을 임포트해서 사용하면 될 것 같은데, 난 굳이 만들어서 썼다. 차이나 오류가 있는지 꼭 확인해보자.
5. 좋아요라던가 여타 기능들을 객체로 끌어다 쓰거나 모델로 잡아야 하는데, 그 부분에서 섬세하지 못했다.
6. 그리고 모델안에서 `blank=True` 라던가 필드 부분들을 섬세하게 작성하지 못했다. 이 부분 역시 수정해야 할 것.

## 논리 vs 물리

일단 쉽게 생각해보면,

- 논리 모델 : 의미명 ( 한글이나 알아보기 쉬운 단어로 표현 )
- 물리 모델 : 실제 칼럼명

근데, 이렇게 생각하면 오류가 나기 쉽다. 왜냐하면 1대1 매핑이 되지 않는 경우가 있기 때문. 편하게 생각하면 이런건데, 조금 더 자세히 생각해보면

### 논리 단계

논리 설계에서는 엔티티와 엔티티타입, 관계를 정의한다.

### 물리 단계

물리 설계단에서는 각 엔티티 관계에 의해서 나올 수 있는 테이블, 즉 실제로 dbms에 생성될 테이블들이 설계가 된다.

그리고, 관계에 대한 정의(ex:CASCADE), 인덱스, 컬럼별 데이터타입 및 제약조건 등의 속성을 정의하고 정규화를 실시한다.

그러니까 논리모델을 실제 dbms에 적용시키는 상세화 과정이라고 생각하면 된다!

## 식별 vs 비식별

### 식별 관계

부모 테이블의 `기본키` 또는 `유니크 키`를 **자식 테이블이 자신의 기본키**로 사용하는 관계.

- 부모 테이블의 키가 자신의 기본키에 포함되기 때문에, 반드시 부모 테이블이 존재해야 자식 테이블에 데이터를 입력할 수 있다.
    
    → 그니까 부모 데이터가 없으면 자식 데이터가 있을 수 없다. 
    
    - `EX` : 자동차와 바퀴.

### 비식별 관계

부모 테이블의 `기본키` 또는 `유니크 키`를 **자신의 기본키로 사용하지 않고**, **외래 키로 사용하는 관계**

- 자식 데이터는 부모 데이터가 없어도 독립적으로 생성될 수 있습니다.
- 부모에 의존하지 않기 때문에 조금 더 자유로운 데이터 생성과 수정이 가능.

### 예시

1. **자동차와 바퀴**
    
    왼쪽, 오른쪽 앞 뒷 바퀴에 타이어를 다 추가 가능
    
    **만약, 개발자가 왼쪽 앞 바퀴에 타이어를 추가 하려고 한다면?**
    
    1. `식별 관계` 의 경우 :
        
        `PK` 는 중복해서 존재할 수 없기 때문에, 데이터 입력 자체가 불가능하다. 
        
        - 장점 : **데이터 정합성** 을 디비에서도 체크할 수 있다.
        - 단점 : 요구사항이 변경되었을 경우 힘들 수 있다. 예를 들면, 갑자기 타이어가 3개씩 달아야 한다면..?
        
    2. `비식별 관계` 의 경우 :
        
        데이터를 입력 가능하다. 왜냐하면 부모에 의존하지 않기 때문에 자유롭게 생성 가능.
        
        - 장점 :
            - 변동적인 요구사항을 수용할 수 있다.
            - 독립적인 자식 데이터 생성가능.
        - 단점 :
            - 정합성을 지키기 위해서는 별도의 비즈니스 로직이 필요하다.
            - 자식 데이터가 존재해도 부모 데이터가 존재하지 않을 수 있다. → 무결성 보장하지 않는다.

## 수정

1. 좋아요 객체 생성
2. 유저아이디 → `author` 로 바꾸고, 기본 `pk` 설정 바꿈.
3. 모델링 전체 수정중 (기본 id값은 제외하고 설정하기)
    - 유저 : 아이디, 비밀번호, 이름, 이메일 속성 갖고있다. 아이디는 중복되면 안되므로 pk로 지정.
    - 프로필 : 유저랑 `1 대 1` 이라고 생각, 왜냐하면 유저마다 프로필은 단 하나씩만 존재하기 때문이다. 그리고 `식별 관계` 라고 생각하는데, 유저가 존재하지 않는데 프로필이란 데이터가 독립적으로 존재할 수 있을까? 독립적으론 아무 의미가 없으며, 단 하나만 존재할 것이기 때문에 요구사항의 변화가 없을 것이라고 생각해서 식별 관계로 정의하였다. 프로필의 엔티티는 유저이름(외래키), 웹사이트, 소개, 전화번호, 성별이 있다. 인스타의 프로필 수정 항목에서 볼 수 있는 것들. 팔로워와 팔로잉은 따로 구현해야 할 것 같다.
    - 게시물 : `비식별` 관계로 정의, 유저와 1대다 관계.
    - 사진, 동영상 : 게시물과 비식별 관계. 1대 다 관계.
    - 좋아요 : 아이디를 기본키로 갖고,
    - 댓글 : 게시물과는 비식별 관계, 댓글은 유저별로 구분이 되니까 유저와는 1대1 관계,
    - 스토리 : 본사람들도 따로 저장해야하니까, 아이디와는 1대1 관계를 맺고 스토리와는 비식별관계를 맺는 1대다 관계의 본사람 모델 정의함.
    - 팔로우, 팔로워 는 어떻게 모델을 작성해야할지 끝까지 완료하지 못했다.

# 4주차 과제

# Serializer

[Django REST framework 시작하기](https://cjh5414.github.io/django-rest-framework/)

(참고자료) → 이건 단순 따라하기 좋게 설명되어 있다.

### 파일 구조

```python
── api
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
├── django-rest-framework-14th
    ├── __init__.py
    ├── asgi.py
    ├── settings
    │   ├── __init__.py
    │   ├── base.py
    │   ├── dev.py
    │   └── prod.py
    ├── urls.py
    └── wsgi.py
```

`api app` 안에 `[serializers.py](http://serializers.py)` 파일을 추가해 주었다.

그리고 `settings/base.py` 에 있는 `INSTALLED_APP` 에 `rest_framework` 를 추가해주면 끝!

### serializers.py

```python
from api.models import Profile
from rest_framework import serializers

class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    website = serializers.CharField(required=False, allow_blank=True, max_length=40)
    introduction = serializers.CharField(allow_blank=True)
    phone_num = serializers.IntegerField(allow_null=False)
    gender = serializers.CharField()

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    def update(self,instance,validated_data):
        instance.website =validated_data.get('website',instance.website)
        instance.introduction = validated_data.get('introduction',instance.introduction)
        instance.phone_num = validated_data.get('phone_num', instance.phone_num)
        instance.gender = validated_data.get('gender',instance.gender)
        instance.save()
        return instance
```

일단은 이정도로 작성해 주었다.

공식문서 튜토리얼을 참고하면서 작성하였다. [https://www.django-rest-framework.org/api-guide/serializers/](https://www.django-rest-framework.org/api-guide/serializers/)

## 실행 결과

![스크린샷 2021-10-14 오후 9.32.11.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/8e4776af-197e-4622-ab28-a9e642f6f46b/스크린샷_2021-10-14_오후_9.32.11.png)

![스크린샷 2021-10-14 오후 9.32.22.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/fd02c27f-f1ec-468d-a730-2d3ee8d287af/스크린샷_2021-10-14_오후_9.32.22.png)

`shell` 에서 실행을 해보니 정상적으로 작동한다.

원래 파라미터들이나, 실행했을 때 오류들도 살펴보고, 내가 원래 설계해놓은 모델링도 수정해야 하는데, 시험기간과 과제를 우선적으로 하다보니 꼼꼼하게 살펴보질 못했다.

어떻게 돌아가는지 어느정도 파악을 했으니, 다음에 깊게 파서 정리해 보겠습니다.

## 4주차 과제
## 모든 객체 나타내기

```python
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
```

`Comment` 에 있는 모든 필드를 나타내고 싶으면, `fields` 에 `__all__` 을 추가하면 된다.

## 에러들

> Forbidden (CSRF cookie not set.): /api/posts
> 

유저가  해당 요청에 대한 권한이 없다는 뜻. 즉, 권한을 인증할만한 토큰 같은것이 필요하다는 것.

### CSRF란 ?

> CSRF는 사이트간 요정 위조를 말한다. 사이트 간 요청 위조는 웹사이트 취약점 공격의 하나로, 사용자가 자신의 의지와는 무관하게 공격자가 의도한 행위를 특정 웹사이트에 요청하게 하는 공격을 말한다. 유명 경매 사이트인 옥션에서 발생한 개인정보 유출 사건에서 사용된 공격 방식 중 하나다
> 

해결할 수 있는 다양한 방법

[https://www.dev2qa.com/how-to-enable-or-disable-csrf-validation-in-django-web-application/](https://www.dev2qa.com/how-to-enable-or-disable-csrf-validation-in-django-web-application/)

우리는 `Function-Based View` 기 때문에,

```python
# views.py

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

def post_view(request):
~~~

```

이렇게 해결해 주었다.

## Post

### GET API

- URL : `api/posts`
- Method : GET

```json
[
    {
        "id": 3,
        "author": {
            "id": 1,
            "username": "sossont",
            "nickname": "0o_hwan",
            "gender": "M",
            "phone_num": 1047426160,
            "introduction": "안녕하세요 정환우 입니다.",
            "website": "http://velog.io/@sossont"
        },
        "location": "Seoul",
        "title": "첫 게시글!",
        "post_likes": [
            {
                "nickname": "test1"
            }
        ],
        "post_comments": [],
        "created_date": "2021-11-01T02:03:33.622916+09:00",
        "updated_date": "2021-11-01T02:03:33.622976+09:00"
    },
    {
        "id": 4,
        "author": {
            "id": 2,
            "username": "test1",
            "nickname": "test1",
            "gender": "M",
            "phone_num": 1039583929,
            "introduction": "test1111",
            "website": "http://velog.io/@test"
        },
        "location": "Dongdaemungu",
        "title": "First Post",
        "post_likes": [
            {
                "nickname": "0o_hwan"
            }
        ],
        "post_comments": [
            {
                "comment": "Wow",
                "nickname": "0o_hwan",
                "created_date": "2021-11-01T02:04:25.779203+09:00"
            }
        ],
        "created_date": "2021-11-01T02:03:49.712405+09:00",
        "updated_date": "2021-11-01T02:03:49.712457+09:00"
    },
    {
        "id": 5,
        "author": {
            "id": 1,
            "username": "sossont",
            "nickname": "0o_hwan",
            "gender": "M",
            "phone_num": 1047426160,
            "introduction": "안녕하세요 정환우 입니다.",
            "website": "http://velog.io/@sossont"
        },
        "location": "우리집",
        "title": "Example 3",
        "post_likes": [
            {
                "nickname": "0o_hwan"
            },
            {
                "nickname": "test1"
            }
        ],
        "post_comments": [
            {
                "comment": "#좋아요 #맞팔",
                "nickname": "0o_hwan",
                "created_date": "2021-11-06T17:07:37.584469+09:00"
            }
        ],
        "created_date": "2021-11-06T17:05:38.455631+09:00",
        "updated_date": "2021-11-06T17:05:38.455668+09:00"
    }
]
```

## POST

- URL : `api/posts`
- Method : POST
- Body

```json
{
    "id" : 6,
    "author" : 1,
    "location" : "Paris",
    "title" : "파리 여행",
    "created_date" : "2021-11-06T12:05:38.455631+09:00",
    "updated_date": "2021-11-06T19:22:11.455668+09:00"
}

```

### 결과

```json
[
    {
        "id": 3,
        "author": {
            "id": 1,
            "username": "sossont",
            "nickname": "0o_hwan",
            "gender": "M",
            "phone_num": 1047426160,
            "introduction": "안녕하세요 정환우 입니다.",
            "website": "http://velog.io/@sossont"
        },
        "location": "Seoul",
        "title": "첫 게시글!",
        "post_likes": [
            {
                "nickname": "test1"
            }
        ],
        "post_comments": [],
        "created_date": "2021-11-01T02:03:33.622916+09:00",
        "updated_date": "2021-11-01T02:03:33.622976+09:00"
    },
    {
        "id": 4,
        "author": {
            "id": 2,
            "username": "test1",
            "nickname": "test1",
            "gender": "M",
            "phone_num": 1039583929,
            "introduction": "test1111",
            "website": "http://velog.io/@test"
        },
        "location": "Dongdaemungu",
        "title": "First Post",
        "post_likes": [
            {
                "nickname": "0o_hwan"
            }
        ],
        "post_comments": [
            {
                "comment": "Wow",
                "nickname": "0o_hwan",
                "created_date": "2021-11-01T02:04:25.779203+09:00"
            }
        ],
        "created_date": "2021-11-01T02:03:49.712405+09:00",
        "updated_date": "2021-11-01T02:03:49.712457+09:00"
    },
    {
        "id": 5,
        "author": {
            "id": 1,
            "username": "sossont",
            "nickname": "0o_hwan",
            "gender": "M",
            "phone_num": 1047426160,
            "introduction": "안녕하세요 정환우 입니다.",
            "website": "http://velog.io/@sossont"
        },
        "location": "우리집",
        "title": "Example 3",
        "post_likes": [
            {
                "nickname": "0o_hwan"
            },
            {
                "nickname": "test1"
            }
        ],
        "post_comments": [
            {
                "comment": "#좋아요 #맞팔",
                "nickname": "0o_hwan",
                "created_date": "2021-11-06T17:07:37.584469+09:00"
            }
        ],
        "created_date": "2021-11-06T17:05:38.455631+09:00",
        "updated_date": "2021-11-06T17:05:38.455668+09:00"
    },
    {
        "id": 6,
        "author": {
            "id": 1,
            "username": "sossont",
            "nickname": "0o_hwan",
            "gender": "M",
            "phone_num": 1047426160,
            "introduction": "안녕하세요 정환우 입니다.",
            "website": "http://velog.io/@sossont"
        },
        "location": "Paris",
        "title": "파리 여행",
        "post_likes": [],
        "post_comments": [],
        "created_date": "2021-11-06T23:55:28.433851+09:00",
        "updated_date": "2021-11-06T23:55:28.433921+09:00"
    }
]
```
# 5주차 과제

## Django Admin 페이지

지난주 스터디 때 다른 분들이 `admin` 페이지를 수정한 것을 보고, 나도 수정을 해보고 싶었다.

구현하고 싶은 것 : `Post`  에서 댓글과 좋아요 개수, 그리고 업로드한 날짜를 확인 하는 것.

먼저 댓글과 좋아요는 `Post` 를 `Foreign Key` 로 참조하고 있기 때문에,  이것을을 `admin` 페이지에서 참조하는 방법이 무엇이 있을까 찾아보았다.

1. `Inline` 을 사용하면 객체 안에서 참조하고 있는 것들을 수정할 수 있다. → 이것을 이용해서 `Comment` 를 안에서 조회 가능.
2. 좋아요와 댓글 개수는 어떻게 참조할 것인가? `quaryset` 을 이용해서 쿼리를 날리고 `annotate` 를 이용하여 카운트를 하면 되는 것 같다.
3. 그냥 `obj.count` 를 이용하는 방법이 있는데, `N+1 problem` 을 야기할 수 있기 때문에, 쿼리를 날리는 것이 안전하다.

## Admin Class로 이용하기

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
```

Admin에 등록하는 방법은 여러가지가 있는데, 이 방법을 가장 선호한다고 한다.

## Inline 사용하기

```python
class CommentInline(admin.TabularInline):
    model = Comment
# Comment 객체를 인라인으로 사용하고 싶기 때문에 이렇게 선언하다.
```

이렇게 인라인을 선언하고, 원래 클래스에서 Inlines 리스트에 이것을 넣으면 된다.

```python
class PostAdmin(admin.ModelAdmin):
	inlines = [CommentInline]
```

이런식으로.

## Count QuarySet 이용하기

```python
def comment_count(self,obj):
        return obj.comment_count

    def like_count(self,obj):
        return obj.like_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(comment_count = Count("post_comments"), like_count = Count("post_likes"))
        return queryset

    comment_count.short_description = "Comments count"
    comment_count.admin_order_field = 'comment_count'   # make the column sortable.
    like_count.admin_order_field = 'like_count'
```

이렇게 선언하면, 카운트 값도 조회가 가능하다.

## 총 코드

```python
from django.contrib import admin
from django.db.models import Count

from .models import *

# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    """
    이 코드는  N+1 problem을 야기하기 때문에 다른 방식을 사용하는 것이 좋다.
    def post_comment_count(self,obj):
        return obj.comment_set.count()
    """
    def comment_count(self,obj):
        return obj.comment_count

    def like_count(self,obj):
        return obj.like_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(comment_count = Count("post_comments"), like_count = Count("post_likes"))
        return queryset

    comment_count.short_description = "Comments count"
    comment_count.admin_order_field = 'comment_count'   # make the column sortable.
    like_count.admin_order_field = 'like_count'
    inlines = [CommentInline]
    list_display = ['id', 'title', 'author', 'comment_count', 'like_count','created_date', 'updated_date']
    list_display_links = ['id','title']
    list_per_page = 10
```

## `Post` 조회

![스크린샷 2021-11-10 오후 10 31 56](https://user-images.githubusercontent.com/69099144/141143839-6540defc-e289-42e4-8be2-739ba40856c6.png)

## Inline

![inline](https://user-images.githubusercontent.com/69099144/141143982-1eb909dc-beb5-420b-9673-6d29ba98f864.png)

`Inline` 선언을 하면 이렇게 이용 가능하다. 신기하다.

# View 수정하기

스터디 시간에도 말했지만 우리는 `FBV` 와 `CBV` 중에 `CBV` 를 이용할 것이다.

[CBV vs FBV](https://www.notion.so/f9f7f594d9404c55a480c6c58d47be5a)

## GET 명령어에 Parameter 받기

1. 일단 처음 찾은 방법은, `url parameter` 을 이용하는 방법이다.

```python
# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('posts/', PostListView.as_view(),name='post-list'),
    path('posts/<int:post_id>', PostDetailView.as_view())
]
```

`<int:post_id>` 라는 것을 추가해, 뒤에 숫자값이오면 `PostDetailView` 에 `post_id` 에 숫자를 넣어 변수를 전달해준다.

```python
# views.py
class PostDetailView(APIView):
    def get(self,request,post_id):
        post_data = Post.objects.filter(id=post_id)
        serializer = PostSerializer(post_data, many=True)
        return JsonResponse(serializer.data, safe=False)
```

그러면, `post_id` 를 filter를 이용해 쿼리를 날려서 값을 찾고, 리턴하게 되는 구조이다. 잘 작동한다.

1. `query parameter`

```python
# views.py
class PostListView(APIView):
    def get(self,request,format=None):
        post_id = request.GET.get('post_id', None)
        if post_id is not None:
            post_data = Post.objects.filter(id=post_id)
        else:
            post_data = Post.objects.all()

        serializer = PostSerializer(post_data, many=True)
        return JsonResponse(serializer.data, safe=False)
```

`request.GET.get` 을 이용해 url에 있는 변수들을 쿼리한다. `.get` 을 쓰면 값이 없는 경우를 대비할 수 있고, 값이 없는 경우가 없다면 `request.GET['post_id']` 로 값을 가져올 수 있다.

값이 없을 경우에 나는 `None` 값을 설정해 주었기 때문에, 값이 없다면 전체를 리턴하고, 아니라면 `filter` 를 적용하여 리턴한다.

잘 작동한다.

### 결과

- 모든 데이터 가져오기. GET `api/posts/`

```json
[
    {
        "id": 3,
        "author": {
            "id": 1,
            "username": "sossont",
            "nickname": "0o_hwan",
            "gender": "M",
            "phone_num": 1047426160,
            "introduction": "안녕하세요 정환우 입니다.",
            "website": "http://velog.io/@sossont"
        },
        "location": "Jeonju",
        "title": "포스트 수정하기",
        "post_likes": [
            {
                "nickname": "test1"
            }
        ],
        "post_comments": [],
        "created_date": "2021-11-01T02:03:33.622916+09:00",
        "updated_date": "2021-11-11T00:04:13.893453+09:00"
    },
    {
        "id": 4,
        "author": {
            "id": 2,
            "username": "test1",
            "nickname": "test1",
            "gender": "M",
            "phone_num": 1039583929,
            "introduction": "test1111",
            "website": "http://velog.io/@test"
        },
        "location": "Dongdaemungu",
        "title": "First Post",
        "post_likes": [
            {
                "nickname": "0o_hwan"
            }
        ],
        "post_comments": [
            {
                "comment": "Wow",
                "nickname": "0o_hwan",
                "created_date": "2021-11-01T02:04:25.779203+09:00"
            },
            {
                "comment": "Fantastic",
                "nickname": "test1",
                "created_date": "2021-11-10T19:56:54.860135+09:00"
            }
        ],
        "created_date": "2021-11-01T02:03:49.712405+09:00",
        "updated_date": "2021-11-10T19:56:54.847623+09:00"
    },
    {
        "id": 5,
        "author": {
            "id": 1,
            "username": "sossont",
            "nickname": "0o_hwan",
            "gender": "M",
            "phone_num": 1047426160,
            "introduction": "안녕하세요 정환우 입니다.",
            "website": "http://velog.io/@sossont"
        },
        "location": "우리집",
        "title": "Example 3",
        "post_likes": [
            {
                "nickname": "0o_hwan"
            },
            {
                "nickname": "test1"
            }
        ],
        "post_comments": [
            {
                "comment": "#좋아요 #맞팔 #반사",
                "nickname": "0o_hwan",
                "created_date": "2021-11-06T17:07:37.584469+09:00"
            }
        ],
        "created_date": "2021-11-06T17:05:38.455631+09:00",
        "updated_date": "2021-11-10T19:57:06.011517+09:00"
    },
    {
        "id": 6,
        "author": {
            "id": 1,
            "username": "sossont",
            "nickname": "0o_hwan",
            "gender": "M",
            "phone_num": 1047426160,
            "introduction": "안녕하세요 정환우 입니다.",
            "website": "http://velog.io/@sossont"
        },
        "location": "Paris",
        "title": "파리 여행",
        "post_likes": [
            {
                "nickname": "0o_hwan"
            }
        ],
        "post_comments": [
            {
                "comment": "파리 가고 싶다,,",
                "nickname": "test1",
                "created_date": "2021-11-10T19:57:21.208848+09:00"
            }
        ],
        "created_date": "2021-11-06T23:55:28.433851+09:00",
        "updated_date": "2021-11-10T19:57:21.207126+09:00"
    },
    {
        "id": 7,
        "author": {
            "id": 1,
            "username": "sossont",
            "nickname": "0o_hwan",
            "gender": "M",
            "phone_num": 1047426160,
            "introduction": "안녕하세요 정환우 입니다.",
            "website": "http://velog.io/@sossont"
        },
        "location": "Paris",
        "title": "파리 여행",
        "post_likes": [],
        "post_comments": [],
        "created_date": "2021-11-10T23:49:23.973382+09:00",
        "updated_date": "2021-11-10T23:49:23.973470+09:00"
    },
    {
        "id": 8,
        "author": {
            "id": 2,
            "username": "test1",
            "nickname": "test1",
            "gender": "M",
            "phone_num": 1039583929,
            "introduction": "test1111",
            "website": "http://velog.io/@test"
        },
        "location": "Paris",
        "title": "파리 여행3",
        "post_likes": [],
        "post_comments": [],
        "created_date": "2021-11-10T23:49:52.674786+09:00",
        "updated_date": "2021-11-10T23:49:52.674823+09:00"
    }
]
```

- URL : `api/posts/5` or `api/posts/?post_id=5`
- Method : `GET`

```json
[
    {
        "id": 5,
        "author": {
            "id": 1,
            "username": "sossont",
            "nickname": "0o_hwan",
            "gender": "M",
            "phone_num": 1047426160,
            "introduction": "안녕하세요 정환우 입니다.",
            "website": "http://velog.io/@sossont"
        },
        "location": "우리집",
        "title": "Example 3",
        "post_likes": [
            {
                "nickname": "0o_hwan"
            },
            {
                "nickname": "test1"
            }
        ],
        "post_comments": [
            {
                "comment": "#좋아요 #맞팔 #반사",
                "nickname": "0o_hwan",
                "created_date": "2021-11-06T17:07:37.584469+09:00"
            }
        ],
        "created_date": "2021-11-06T17:05:38.455631+09:00",
        "updated_date": "2021-11-10T19:57:06.011517+09:00"
    }
]
```

## CREATE

- URL : `api/posts/`
- Method : `POST`
- Body :

```json
{
"author" : 1,
"location" : "Jeonju",
"title" : "포스트 수정하기"
}
```

### 결과

```json
{
    "id": 10,
    "author": {
        "id": 1,
        "username": "sossont",
        "nickname": "0o_hwan",
        "gender": "M",
        "phone_num": 1047426160,
        "introduction": "안녕하세요 정환우 입니다.",
        "website": "http://velog.io/@sossont"
    },
    "location": "Jeonju",
    "title": "포스트 수정하기",
    "post_likes": [],
    "post_comments": [],
    "created_date": "2021-11-11T00:23:59.492435+09:00",
    "updated_date": "2021-11-11T00:23:59.492472+09:00"
}
```

## PUT

앞에서 원리를 좀 이해하니까 금방금방 작성이 가능하다.

```python
# views.py

class PostDetailView(APIView):
    def put(self,request,post_id):
        if post_id is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            post_object = Post.objects.get(id=post_id)
            update_post_serializer = PostSerializer(post_object,data=JSONParser().parse(request))
            if update_post_serializer.is_valid():
                update_post_serializer.save()
                return JsonResponse(update_post_serializer.data, status=201)
            else:
                return JsonResponse(update_post_serializer.errors, status=400)
```

`post_id` 값이 없으면 오류를 반환하고, 아니면 `post_id` 를 이용해 객체를 조회해서, 업데이트 작업을 한다.

위에서 방금 만든거 수정해보자.

- URL : `api/posts/<int:pk>`
- Method : `PUT`
- Body :

```json
{
    "author" : 2,
    "location" : "London",
    "title" : "풋풋"
}
```

### 결과

```json
{
    "id": 10,
    "author": {
        "id": 2,
        "username": "test1",
        "nickname": "test1",
        "gender": "M",
        "phone_num": 1039583929,
        "introduction": "test1111",
        "website": "http://velog.io/@test"
    },
    "location": "London",
    "title": "풋풋",
    "post_likes": [],
    "post_comments": [],
    "created_date": "2021-11-11T00:23:59.492435+09:00",
    "updated_date": "2021-11-11T00:25:31.720960+09:00"
}
```

## DELETE

```python
class PostDetailView(APIView):
    def delete(self, request, post_id):
        try:
            post_object = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            post_object = None

        if post_object is None:
            return Response("No Content Request", status=status.HTTP_204_NO_CONTENT)
        else:
            post_object.delete()
            return Response("Delete Success",status=status.HTTP_200_OK)
```

Notion에 적혀있는대로 없으면 status 204를 반환하고,  있으면 지우고 status 200을 반환한다.

- URL : `api/posts/<int:pk>`
- Method : `DELETE`
- ex : `api/posts/4`

### 결과

<img width="927" alt="스크린샷 2021-11-11 오전 12 27 24" src="https://user-images.githubusercontent.com/69099144/141143715-8a6542a3-f112-4923-a119-4167a08510e1.png">

지워졌으니 한번 더 해보자.

![204](https://user-images.githubusercontent.com/69099144/141144065-41f27aeb-4778-4e74-87d5-75697be28a63.png)

204 에러 발생. 제대로 작동한다.

## 발생한 이슈들

1. `AttributeError: 'function' object has no attribute 'as_view'`  : 분명히 제대로 했는데 왜 안되는가 했었는데, 저번에 뷰 짤때 넣었던 decorator인 `@csrf_exmept` 가 함수를 반환해서 안되는 것이었다. 지워주니 해결 되었다.

하나를 제대로 구현하니까 나머지들도 쭉쭉 이해가 되기 시작했다. 이거 뷰 꾸미는거 되게 재밌는 것 같다. 부가기능도 더 구현해봐야겠다. `query` 에 관한 이해가 중요할 것 같다.
