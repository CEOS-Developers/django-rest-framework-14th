## 1. 인스타그램 서비스에 대한 설명

* ###인스타그램: 페이스북에서 운영하고 있는 **이미지** 공유 중심의 미국의 소셜 미디어입니다.  

</br>

>주요 기능
>>* 사용자는 사진 및 짧은 동영상을 업로드할 수 있다. **(사진 및 동영상 업로드 기능)**
>>* 다른 사용자의 피드를  팔로잉할 수 있다. **(팔로우-팔로잉 기능)**
>>* 위치 이름으로 이미지를 지오태그(geotag)할 수 있다. **(태그 기능)**
>>* 사용자는 자신의 인스타그램 계정을 다른 SNS 사이트에 연결하여 업로드한 사진을 해당 사이트에 공유할 수 있다.
</br>


## 2. SQL의 제약 조건 & ERD
* **제약조건**이란: 데이터를 다룰 때 어떠한 제약을 두는 것입니다.
* 제약조건을 사용하는 이유: 데이터의 **무결성**을 지키기 위해서 제한된 조건을 겁니다.   
  (데이터의 무결성: 데이터의 정확성, 일관성, 유효성이 유지되는 것)   
   -> 그래서 특정 데이터를 입력할 때 어떠한 조건을 만족했을 때만 입력되도록 제약할 수 있습니다.
* 제약조건: Primary Key, Foreign Key, Unique, Default, Null
</br>
</br>


##2.1 Primary Key(기본키)
> Primary Key (기본키)
>> 테이블에 존재하는 많은 행의 데이터를 구분할 수 있는 **식별자** 입니다.   
> 
>> 중복되서도 안되며 비어서도 안됩니다.   

* 기본키는 테이블에서 하나 이상의 열에 설정할 수 있습니다.
* Primary Key(이하PK)는 식별자인 만큼 데이터 튜플에 대한 접근을 할 수 있는 지표입니다.

### PK를 설정 시 고려해야할 점
* 데이터의 값이 자주 바뀌면 안됩니다.
* PK의 값이 단순한 값이 좋습니다.
</br>
</br>

##2.2 Foreign Key(외래키)
> Foreign Key (외래키)
>> 한 테이블의 키 중에서 다른 테이블의 레코드를 유일하게 식별할 수 있는 키입니다.
</br>

![외래키 예시](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbFsihj%2FbtqEanqDCI3%2FURLUyUai7llnOQhfRw2GW0%2Fimg.png)
* 외래 키 관계를 설정하면 하나의 테이블(자식 테이블)이 다른 테이블(부모 테이블)에 **의존**하게 됩니다.
* 자식 테이블에서 부모 테이블로 조건을 추가하게 되고, 자식 테이블(외래키 포함된 테이블)에서 조건을 걸어주면 됩니다.


> 외래키 수정/삭제 시 연결된 데이터 처리 방법
>> RESTRICT: 변경/삭제가 취소(거부)   
> 
>> CASCADE: 함께 변경/삭제   
> 
>> NO ACTION: 변경/삭제할 개체만 변경/삭제되고 참조하고 있는 개체는 변동이 없음  
> 
>> SET NULL: 참조하고 있는 값은 NULL로 세팅


</br>
</br>

##2.3 외래 키를 사용하여 테이블 간 관계를 정립하기 - 식별 관계, 비식별 관계

> **식별 관계**
>> 부모 테이블의 기본키 또는 유니크 키를 자식 테이블이 자신의 기본키(PK)로 사용하는 관계

</br>

![식별 관계](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FYioAe%2FbtqFPriMerk%2FFrSpo08ZHl2KpDTg2ReIxK%2Fimg.png)

* 부모 테이블의 키가 자신의 기본키에 포함되기 때문에,   
  반드시 부모 테이블에 데이터가 존재해야 자식 테이블에 데이터를 입력할 수 있습니다.
* 즉, 부모 데이터가 없다면 자식 데이터는 생길 수 없습니다.   
</br>
* 식별관계는 ERD상에서 **실선**으로 표시합니다.
* 자식 테이블에 데이터가 존재한다면 부모 데이터가 반드시 존재하는 상태가 됩니다.   
-> 즉, 자식 테이블이 부모 테이블에 **종속**됩니다.   
</br>
</br>

> **비식별 관계**
>> 부모 테이블의 기본키 또는 유니크 키를 자신의 기본키로 사용하지 않고, 외래 키로 사용하는 관계

</br>

![비식별 관계](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcFZ1cV%2FbtqFOWQQR80%2F5bf3sjjPznGDUz0kSIpQck%2Fimg.png)

* 자식 데이터는 부모 데이터가 없어도 독립적으로 생성될 수 있습니다.
* 부모와의 의존성을 줄일 수 있기 때문에 조금 더 자유로운 데이터의 생성과 수정이 가능합니다.


### 각각의 장단점 비교

> 식별 관계의 장점
* 데이터의 정합성 유지를 DB에서 한번 더 할 수 있다.
* 자식 테이블에 데이터가 존재한다면 부모 데이터도 반드시 존재한다고 보장할 수 있다.

> 식별 관계의 단점
* 요구사항이 변경되었을 경우 구조 변경이 어렵다.

> 비식별 관계의 장점
* 변경되는 요구사항을 유동적으로 수용할 수 있다.
* 부모 데이터와 **독립적인** 자식 데이터를 생성할 수 있다.

> 비식별 관계의 단점
* 데이터의 정합성을 지키기 위해서는 별도의 비즈니스 로직이 필요하다.
* 자식 데이터가 존재해도 부모 데이터가 존재하지 않을 수 있다.
* 즉, 데이터 무결성을 보장하지 않는다.





## 3. '사진, 영상 업로드'라는 핵심 기능에 집중한 인스타그램 모델링

> ### 모델1. Profile
기존 User 모델을 OneToOne Relation을 맺어 Profile 모델을 구상하였습니다.   
먼저, 직접 인스타그램에 들어가 Profile에 필요한 field들을 찾아보았습니다.   
![profile1](https://postfiles.pstatic.net/MjAyMTEwMDdfMzkg/MDAxNjMzNTkzOTAzMzk4.1RGuFolQ7WS-FzFpfXlWP_M9ph8Q9Av4LBWXPW6X8hAg.hHwvXcggGToXiTI3c6ho4AXMyOzjDDeH0wSQm9_r-Owg.PNG.sssssjin99/image.png?type=w966)
![profile2](https://postfiles.pstatic.net/MjAyMTEwMDdfNTQg/MDAxNjMzNTkzOTEzMTU5.hAb4vD4kYpGL5WO4zRqjP41Q3hhM4bOHfHhUt-POzRwg.pgtchqAQOWx4k2rMY3zs0860DpSjXlRkGVM3DfepHV0g.PNG.sssssjin99/image.png?type=w966)

필요한 field들은 다음과 같습니다.   

|**Field**|내용값|  |Profile 모델에 들어갈 값|
|-------|--------|-----|--------|
|이름|수지니| |(user model의) username|
|비밀번호|****| |(user model의) password|
|프로필 사진|(이미지 파일)| |photo|
|사용자 이름|ssssujini99| |nickname|
|웹사이트| | | website|
|소개|반갑습니다*^^*| |intro|
|이메일|sssssjin99@naver.com| |email|
|전화번호|+821090489745| |phone_num|
|성별|여성| |gender|

이를 구현한 모델은 다음과 같습니다.
```
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
```

</br>

> ### 모델2. Post
모델 Post는 '게시글'과 관련된 모델입니다.   
게시글을 작성하기 위해서 필요한 것은   
**ⓐ글쓴이(author) ⓑ사진(photo) ⓒ내용(content) ⓓ최초 작성 시간(created_at) ⓔ최종 수정 시간(updated_at)**  
라고 생각했습니다.

코드로 구현한 모델은 다음과 같습니다.   

이때, Profile와 Post의 관계는 One to Many 입니다.


```angular2html
# 게시글 모델 구현
class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE) # 글쓴이 ## Profile - Post : One to Many 관계
    photo = models.ImageField(upload_to = "post") # 사진
    content = models.CharField(max_length=300, help_text="최대 길이 300자 입력이 가능합니다.") # 내용
    created_at = models.DateTimeField(auto_now_add = True) # 최초 작성 시간
    updated_at = models.DateTimeField(auto_now = True) # 최종 수정 시간
```
</br>

> ### 모델3. Like
모델 Like는 '좋아요'와 관련된 모델입니다.   
모델 Like는 Profile모델, Post모델과 각각 일대다(OneToMany)관계에 있는 모델입니다.   
외래키로 Profile모델과 Post모델을 참조하였습니다.

```angular2html
# 좋아요 모델 구현
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 해당 게시글 ## Post - Like : One to Many 관계
    user = models.ForeignKey(Profile, on_delete=models.CASCADE) # 좋아요를 누른 사용자 ## Profile - Like : One to Many 관계
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
```
</br>

> ### 모델4. Comment
모델 Comment는 '댓글'과 관련된 모델입니다.   
모델 Comment는 Profile모델, Post모델과 일대다(OneToMany)관계에 있는 모델입니다.   
외래키로 Profile모델과 Post모델을 참조하였습니다.   

```angular2html
# 댓글 모델 구현
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 해당 게시글 ## Post - Comment : One to Many 관계
    author = models.ForeignKey(Profile, on_delete=models.CASCADE) # 댓글을 쓴 사용자 ## Profile - Comment : One to Many 관계
    content = models.CharField(max_length=50) # 댓글 내용
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
```
</br>


> ### 모델5. Bookmark
모델 Bookmark는 '북마크'와 관련된 모델입니다.   
외래키로 Post모델과 Profile모델을 참조하였습니다.

```angular2html
# 북마크 모델 구현
class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
```

</br>


> ### 모델6. Follow
모델 Follow는 인스타그램의 '팔로우'와 관련된 모델입니다.   
코드리뷰 이후에, 혜원님께서 작성하신 팔로우 모델링을 기반으로 저도 공부를 하고 팔로우 모델을 만들게 되었습니다.   

```angular2html
# 팔로우 모델 구현
class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return '{} -> {}'.format(self.follower.nickname, self.following.nickname)
```

예를들어, a가 b에게 팔로우를 걸면  
위의 모델 테이블에 a->b, b->a의 두 개의 테이블이 작성되도록 만들 예정입니다.   
이 방법 말고도, 더 좋은 모델링 방법을 생각해보고 있습니다.   
이 **팔로우** 모델링에 대해서는 추가적인 공부가 더 필요하다고 생각합니다.

</br>
</br>

## 4. ERD 직접 만들어보기
원래 모델링을 하기 전에 먼저 해야하는 것이 ERD이지만,   
저는 ERD가 처음이라 이에대한 문법이나 만드는 방법을 뒤늦게 찾아보고 이후에 작성하게 되었습니다.   

원래는 데이터베이스 설계 이전에, ERD를 사용하여 전체 데이터 베이스의 구조를 먼저 잡고   
이후에 진행해야하지만   
이번에는 뒤늦게 ERD 툴을 이용하여 작성하게 되었습니다.

ERD를 작성하는 툴을 먼저 익힌 후에, 작성하게 되었습니다.





</br>

## 5. ORM 이용해보기
```angular2html
(venv) PS C:\Users\82109\Desktop\docker\django-rest-framework-14th> python manage.py shell
Python 3.9.0 (tags/v3.9.0:9cf6752, Oct  5 2020, 15:34:40) [MSC v.1927 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from insta.models import Profile, Post, Like, Bookmark, Comment
>>> c1 = Comment(post_id=2, author_id=1, content="댓글1")
>>> c1
<Comment: Comment object (None)>
>>> c1.save()
>>> c2 = Comment(post_id=2, author_id=1, content="댓글2")
>>> c2.save()
>>> c3 = Comment(post_id=3, author_id=1, content="댓글3")
>>> Comment.objects.all()
<QuerySet [<Comment: Comment object (1)>, <Comment: Comment object (2)>]>
>>> c3.save()
>>> Comment.objects.all()
<QuerySet [<Comment: Comment object (1)>, <Comment: Comment object (2)>, <Comment: Comment object (3)>]>
>>> c = Comment.objects.filter(post_id=2)
>>> c
<QuerySet [<Comment: Comment object (1)>, <Comment: Comment object (2)>]>
>>> c = Comment.objects.filter(post_id=3)
>>> c
<QuerySet [<Comment: Comment object (3)>]>
>>> c.id
>>> c = Comment.objects.filter(post_id=2)
>>> c
<QuerySet [<Comment: Comment object (1)>, <Comment: Comment object (2)>]>
>>> c[1]
<Comment: Comment object (2)>
>>> c[1].id
2
>>> c[1].content
'댓글2'
>>> c[1].author_id
1
>>> c[1].post_id
2
>>>
```

</br>

## 6. 간단한 회고

