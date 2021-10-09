## 1. 인스타그램 서비스에 대한 설명

* ###인스타그램: 페이스북에서 운영하고 있는 **이미지** 공유 중심의 미국의 소셜 미디어입니다.  

</br>

>주요 기능
>>* 사용자는 사진 및 짧은 동영상을 업로드할 수 있다. **(사진 및 동영상 업로드 기능)**
>>* 다른 사용자의 피드를  팔로잉할 수 있다. **(팔로우-팔로잉 기능)**
>>* 위치 이름으로 이미지를 지오태그(geotag)할 수 있다. **(태그 기능)**
>>* 사용자는 자신의 인스타그램 계정을 다른 SNS 사이트에 연결하여 업로드한 사진을 해당 사이트에 공유할 수 있다.


## 2. '사진, 영상 업로드'라는 핵심 기능에 집중한 인스타그램 모델링

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

그리고 아래에 **좋아요(Like)모델**, **댓글(Comment)모델**이 있는데,   
게시글(Post)모델은 이 두개의 모델과 **다대다(ManyToMany)관계**를 맺기 때문에   
이도 게시글 모델에 같이 설정해주었습니다.   

코드로 구현한 모델은 다음과 같습니다.   


```angular2html
# 게시글 모델 구현
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 글쓴이
    photo = models.ImageField(upload_to = "post") # 사진
    content = models.CharField(max_length=300, help_text="최대 길이 300자 입력이 가능합니다.") # 내용
    created_at = models.DateTimeField(auto_now_add = True) # 최초 작성 시간
    updated_at = models.DateTimeField(auto_now = True) # 최종 수정 시간

    # many-to-many 모델 연결시키기
    likes = models.ManyToManyField('Like', related_name='like_posts', blank=True)
    comments = models.ManyToManyField('Comment', related_name='comment_posts', blank=True)
```
</br>

> ### 모델3. Like
모델 Like는 '좋아요'와 관련된 모델입니다.   
모델 Like는 Post모델과 다대다(ManyToMany)관계에 있는 모델입니다.   
외래키로 User모델과 Post모델을 참조하였습니다.

```angular2html
# 좋아요 모델 구현
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
```
</br>

> ### 모델4. Comment
모델 Comment는 '댓글'과 관련된 모델입니다.   
모델 Comment는 Post모델과 다대다(ManyToMany)관계에 있는 모델입니다.   
외래키로 User모델과 Post모델을 참조하였습니다.   

```angular2html
# 댓글 모델 구현
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
```
</br>


> ### 모델5. Bookmark
모델 Bookmark는 '북마크'와 관련된 모델입니다.   
외래키로 Post모델과 User모델을 참조하였습니다.

```angular2html
# 북마크 모델 구현
class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
```

</br>


## 3. ORM 이용해보기
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

## 4. 간단한 회고

