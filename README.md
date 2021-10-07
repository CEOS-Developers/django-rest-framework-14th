## 인스타그램 모델링

먼저, 인스타그램 어플에 접속하여 어떠한 항목들이 있는지 정리해보았다.

![스크린샷 2021-10-08 오전 2.12.23.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/d235c3ee-4289-4622-813d-5c6c7e53438c/스크린샷_2021-10-08_오전_2.12.23.png)

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

![스크린샷 2021-10-08 오전 2.10.56.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/d1abb692-f1e5-45f5-85d3-faaa5278836e/스크린샷_2021-10-08_오전_2.10.56.png)

포스트 객체 생성하기

### 필터 적용해보기

![스크린샷 2021-10-08 오전 2.12.00.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/68b120de-4e68-4197-b687-ee17b524bb31/스크린샷_2021-10-08_오전_2.12.00.png)

필터

## 회고

장고를 처음 사용해보고, 모델링도 거의 처음해봤는데, 나름 만족스럽지만 하다보니 계속 고민되는 부분과 아쉬운 부분이 많았다. 피드백을 받는게 기대가 되며, 주말동안 더 수정을 해보려고 한다.
그리고 어떻게 구조가 짜여지는 지 어느정도 느낌이 오는 것 같다. 공부 많이 해야겠다.