# 2주차 모델링과 Django ORM
## 인스타그램
인스타그램은 사진 공유를 기반으로 한 소셜 미디어이다. 

모델링을 진행하기 위해 인스타그램의 핵심 기능을 정리해 보았다. 
- 사진 및 동영상이 포함된 게시글 공유
- 게시글에 좋아요 표시
- 게시글에 댓글 달기
- 다른 사용자를 팔로우 하기

이외에도 해시태그, 미디어에 타 사용자 태그, 비밀 계정, 24시간 동안만 게시물을 확인할 수 있는 스토리 등등 더욱 많은 기능이 있으나 가장 중점적이라고 생각하면서 구현 가능한 기능만 뽑아서 정리했다. 
## 모델링
정리한 핵심 기능을 기반으로 모델을 구성했다. 
### 사용자 - User/Profile
가장 관계가 복잡하고 가장 기본이 되는 모델이다. 

#### Attributes
- account_name: 인스타그램의 사용자 이름(계정 ID)
- phone: 전화번호
- bio: 바이오 (Optional)
- profile_photo: 프로필 사진 (Optional)

User - Profile을 1:1 관계로 설정하는 방식을 사용하였으므로 Django의 기본 모델 User가 가지고 있는 어트리뷰트들은 제외하고 Profile이 가진 어트리뷰트만 나열했다. 
#### Relations
사용자는 게시글을 업로드 할 수 있고 게시글에 좋아요를 표할 수 있으며, 댓글을 남길 수 있다. 또한 타 사용자를 팔로우 할 수 있다. 

- 사용자 - 게시글 → `1:N`
- 사용자 - 좋아요 → `1:N`
- 사용자 - 댓글 → `1:N`
- 사용자 - 팔로잉/팔로워 → `1:N`
### 게시글 - Post
#### Attributes
- caption: 게시글 내용 (Optional)
- date_posted: 게시글을 올린 일시
  - `DateTimeField`의 `auto_now_add`를 사용하여 자동으로 채워지도록 구현했다.
#### Relations
게시글은 하나 이상의 사진이나 동영상을 포함하고 있다. 

- 게시글 - 사진 → `1:N`
- 게시글 - 동영상 → `1:N`
- 게시글 - 좋아요 → `1:N`
- 게시글 - 댓글 → `1:N`
### 사진 - Photo
#### Attirbutes
- image_file: 이미지 파일
### 동영상 - Video
#### Attributes
- video_file: 동영상 파일

`ImageField`가 따로 존재하는 사진과는 달리 동영상 파일은 `FileField`를 통해 받아야 한다. 따라서 `django.core.validators`의 `FileExtensionValidator`를 이용하여 MOV, avi, mp4, webm, mkv의 확장자를 가진 비디오 파일만 업로드 할 수 있도록 했다. 
### 좋아요 - Like
별도의 어트리뷰트 없이 FK 만으로 구성된 모델이다. 
### 댓글 - Comment
#### Attributes
- content: 댓글 내용
### 팔로우 관계 - FollowRelation
구현이 가장 힘들었던 모델이다. 

- follower: 팔로우를 한 사용자
- followee: 팔로우를 당한 사용자

의도하고 싶었던 것은 Django ORM을 통해 `p.followings.all()`(이때, p는 어떤 사용자(Profile)) 이렇게 불러왔을때 사용자 p가 팔로우 하고 있는 모든 Profile 모델을 불러오는 것이었다. 

```python
follower = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='followings')
followee = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='followers')
```

그러나 이렇게 구현하면 `p.followings.all()`을 하면 Profile 모델이 아닌 FollowRelation 모델을 불러오게 된다. 가장 애를 먹었던 문제였는데, 

```python
Profile.add_to_class('followings', models.ManyToManyField('self', through=FollowRelation, related_name='followers', symmetrical=False))
```

이 코드를 추가해 줌으로 해결했다. 

코드를 살펴보면, `add_to_class`는 어트리뷰트를 추가하는 것이 아닌, 메서드를 추가하는 메서드이다. 즉 followings는 존재하는 어트리뷰트가 아니지만, Profile의 메서드로써 어트리뷰트로 불러올 때와 유사하게 동작하게 된다. `ManyToManyField`를 self로 설정하게 되면 Profile은 Profile과 FollowRelation 을 통해 다대다 관계를 맺게되며, 이에 대해 역으로 연결된 객체를 불러 올 때는 followers로 불러 올 수 있는 것이다. 여기서 `ManyToManyField`의 경우 기본적으로 symmetrical 옵션이 True로 설정되어 있는데, 그렇게 되면 profile1이 profile2를 팔로우 할 경우 자동으로 profile2 또한 profile1을 팔로우하게 된다. 따라서 symmetrical 옵션을 False로 반드시 설정해 주어야 한다. 

이러한 설정을 통해 원하던 대로 followers, followings를 아래 처럼 불러올 수 있게 되었다. 

<img width="831" alt="Screen Shot 2021-10-08 at 3 56 43 PM" src="https://user-images.githubusercontent.com/53527600/136519103-c5644a6a-901b-4e9d-bdf7-dedb810e7447.png">

## ORM 이용해보기
### 소스 코드
```python
post = Post.objects.all().first()

comment1 = Comment(profile=Profile.objects.filter(id=1).first(), post=post, content="first comment")
comment1.save()

comment2 = Comment(profile=Profile.objects.filter(id=2).first(), post=post, content="second comment")
comment2.save()

comment3 = Comment(profile=Profile.objects.filter(id=3).first(), post=post, content="third comment")
comment3.save()

Comment.objects.all()
```
### 결과 화면
<img width="1334" alt="Screen Shot 2021-10-08 at 6 02 32 PM" src="https://user-images.githubusercontent.com/53527600/136529246-85231244-71ef-4bbc-b2bd-eccc6325c77c.png">

## 간단한 회고
관계 설정에 생각보다도 많은 시간을 쏟은 것 같다. 그만큼 관계 설정이 어려운 과정이기도 하고, 또한 매우 중요하다는 것을 알게 되었다. FollowRelation 구현이 가장 어려웠고 시간을 많이 썼는데, 아직도 해당 관계 구현에 대해서 100% 만족스럽게 이해를 하지는 못한 것 같아서 아쉽다. 더 많이 공부를 해야 할 것 같다. 
