# 4주차 DRF1 : Serializer
## 과제
### 데이터 삽입
```python
# api/models.py

class Post(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(max_length=2200, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.account_name}'s post: {self.caption}"


class Photo(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='photos')
    image_file = models.ImageField(upload_to='posts/photos')

    def __str__(self):
        return f"Photo from {self.post.profile.account_name} 's post: {self.post.caption}"
```
![Screen Shot 2021-10-15 at 1 55 46 PM](https://user-images.githubusercontent.com/53527600/137434974-446db017-0136-4df5-8554-97ee62abe6ef.png)

### 모든 데이터를 가져오는 API
- URI: `/api/posts/`
- Method: `GET`
![Screen Shot 2021-10-15 at 2 31 30 PM](https://user-images.githubusercontent.com/53527600/137437162-944c1032-8927-4bc1-a870-de817689797b.png)
```JSON
[
    {
        "id": 1,
        "account_name": "admin_profile",
        "profile_photo": "profiles/tmp4et5jeut.jpg",
        "photos": [
            {
                "id": 1,
                "image_file": "/media/posts/photos/01_3oDQNH2.png"
            },
            {
                "id": 2,
                "image_file": "/media/posts/photos/02_JI81FE0.png"
            },
            {
                "id": 3,
                "image_file": "/media/posts/photos/03_aNTXhFi.png"
            }
        ],
        "caption": "첫번째 포스트 ",
        "likes_count": 0,
        "comments_count": 0,
        "date_posted": "2021-10-15T12:53:03.748582+09:00"
    },
    {
        "id": 2,
        "account_name": "admin_profile",
        "profile_photo": "profiles/tmp4et5jeut.jpg",
        "photos": [
            {
                "id": 4,
                "image_file": "/media/posts/photos/01_kQBNcRx.png"
            },
            {
                "id": 5,
                "image_file": "/media/posts/photos/02_C82apOq.png"
            },
            {
                "id": 6,
                "image_file": "/media/posts/photos/03_eOshgZ8.png"
            }
        ],
        "caption": "first post",
        "likes_count": 0,
        "comments_count": 0,
        "date_posted": "2021-10-15T12:53:24.608748+09:00"
    },
    {
        "id": 3,
        "account_name": "test0",
        "profile_photo": "profiles/tmp4et5jeut.jpg",
        "photos": [
            {
                "id": 7,
                "image_file": "/media/posts/photos/02_fal5dwA.png"
            },
            {
                "id": 8,
                "image_file": "/media/posts/photos/03_g7x2K2i.png"
            }
        ],
        "caption": "포스트 테스트",
        "likes_count": 0,
        "comments_count": 0,
        "date_posted": "2021-10-15T13:04:08.731269+09:00"
    },
    {
        "id": 4,
        "account_name": "test0",
        "profile_photo": "profiles/tmp4et5jeut.jpg",
        "photos": [
            {
                "id": 9,
                "image_file": "/media/posts/photos/02_wxXsBO1.png"
            },
            {
                "id": 10,
                "image_file": "/media/posts/photos/03_jydBElM.png"
            }
        ],
        "caption": "포스트 테스트",
        "likes_count": 0,
        "comments_count": 0,
        "date_posted": "2021-10-15T13:06:01.576258+09:00"
    },
    {
        "id": 5,
        "account_name": "test1",
        "profile_photo": "profiles/01_3EM0f2k.png",
        "photos": [
            {
                "id": 11,
                "image_file": "/media/posts/photos/01_xPKDAkw.png"
            },
            {
                "id": 12,
                "image_file": "/media/posts/photos/02_oH3Xsw9.png"
            }
        ],
        "caption": "포스틱포스트",
        "likes_count": 1,
        "comments_count": 1,
        "date_posted": "2021-10-15T13:08:49.525477+09:00"
    }
]
```

### 새로운 데이터를 create하도록 요청하는 API 
- URI: `api/posts/`
- Method: `POST`
- 요청 시 body에 들어가야 하는 필드
  - profile_id: int
  - image_files: file(image)
  - caption: string
![Screen Shot 2021-10-15 at 1 10 07 PM](https://user-images.githubusercontent.com/53527600/137435262-6acc088c-d4fd-4281-b82f-b8a660e73094.png)
```JSON
{
    "id": 5,
    "account_name": "test1",
    "profile_photo": "profiles/01_3EM0f2k.png",
    "caption": "포스틱포스트",
    "likes_count": 1,
    "comments_count": 1,
    "date_posted": "2021-10-15T13:08:49.525477+09:00",
    "photos": [
        {
            "id": 11,
            "image_file": "/media/posts/photos/01_xPKDAkw.png"
        },
        {
            "id": 12,
            "image_file": "/media/posts/photos/02_oH3Xsw9.png"
        }
    ],
    "comments": [
        {
            "id": 1,
            "post_id": 5,
            "account_name": "admin_profile",
            "content": "포스틱 맛있겠네요ㅎ"
        }
    ]
}
```

### 반환되는 JSON의 차이
URI는 같더라도 각 요청에 따라 반환되는 JSON이 조금씩 다르도록 설계했다. 인스타그램 클론이기 때문에 실제 인스타그램 서비스를 생각해 봤을 때 클라이언트에서 각 화면을 구성할 때 실제로 필요할 것 같은 정보를 반환하는 형식으로 구현했다.

#### GET api/posts/
실제 인스타그램의 경우 해당 사용자가 팔로우 하는 계정의 포스트만 보이도록 쿼리를 하겠지만, 일단 지금은 모든 포스트를 가져올 것이라고 가정했다. 인스타그램의 피드에 들어가면 보이는 포스트는 `해당 포스트를 올린 사용자(계정 username), 해당 계정의 프로필 사진, 포스트 내용, 해당 포스트에 포함된 모든 미디어, 좋아요 수, 댓글 수, 일부 댓글, 좋아요를 누른 사용자 일부, 포스트를 올린 시각(...ago 형식)` 이렇게 구성된다. 

실제 인스타그램의 구성에서 내가 기술적으로 구현하기 힘든 부분은 제외하고 재구성 해 보았다. 내가 만든 인스타그램 클론은 아래와 같은 형식의 JSON을 반환한다.
```JSON
{
    "id": <Post id>,
    "account_name": <Profile의 account_name>,
    "profile_photo": <Profile의 profile_photo>,
    "photos": [
        {
            "id": <Photo id>,
            "image_file": <Photo의 image_file>
        },
        ...
    ],
    "caption": <게시글 내용>,
    "likes_count": <좋아요 수>,
    "comments_count": <댓글 수>,
    "date_posted": <게시글을 올린 시각>
}
```

#### POST api/posts/
`POST` 시 반환되는 JSON은 `GET api/post/<int:post_id>/`를 했을 때 반환되는 것과 같다. 댓글 목록이 추가되었다. 실제 인스타그램은 댓글을 쓴 사용자의 프로필 사진도 함께 보여주므로, 댓글 반환 시에 댓글을 쓴 사용자의 `profile_photo`도 함께 반환할 수 있도록 구현하고 싶었는데 아직 방법을 찾지 못했다. 
```JSON
{
    "id": <Post id>,
    "account_name": <Profile의 account_name>,
    "profile_photo": <Profile의 profile_photo>,
    "caption": <게시글 내용>,
    "likes_count": <좋아요 수>,
    "comments_count": <댓글 수>,
    "date_posted": <게시글을 올린 시각>,
    "photos": [
        {
            "id": <Photo id>,
            "image_file": <Photo의 image_file>
        },
        ...
    ],
    "comments": [
        {
            "id": <Comment id>,
            "post_id": <Post id>,
            "account_name": <Profile의 account_name>,
            "content": <댓글 내용>
        }
    ]
}
```

## 회고
### 처음에 ViewSet을 쓰게 된 경위
예전에 DRF를 한 번 써본적이 있었는데, 그때 browsable API가 상당히 신기하고 편했던 기억이 있었다. 그래서 이번에도 DRF를 사용하면 browsable API를 볼 수 있겠지 생각하고 작업했는데 못생기고 밋밋한 화면만 나왔다. 

|기대했던 화면|코드 작성 후 보이는 화면|
|----------|-------------------|
|![robotgetbrwapi-660x452](https://user-images.githubusercontent.com/53527600/137432589-3affc283-0bee-430b-9ab4-08982a30afff.png)|![Screen Shot 2021-10-15 at 1 46 02 PM](https://user-images.githubusercontent.com/53527600/137433650-3bfae81b-69e8-44a3-aae8-c0be434234da.png)|

검색 해 보니 `ViewSet`을 사용하면 browsable API를 사용할 수 있다고 하였다. 심지어 지정된 액션으로 맵핑만 해 주면 정말 간단하고 짧은 뷰 작성만으로도 CRUD를 해 낼 수 있었다! 그래서 열심히 적용을 했으나...

### ViewSet을 다시 적용 해제 한 이유
모델링 해 놓은 것에 맞추다 보니 생각보다 커스텀 해야 할 것이 많았다. 심지어 아직 Django와 DRF에 대한 이해가 부족한 상태인데, 무지성으로 ViewSet을 따라하려 하다 보니 조금 힘들었다. 심지어 `ViewSet`을 적용하게 된 이유인 browsable API로는 `POST` 액션을 테스트 할 수 없어서 `api/tests.py`에 테스트 코드를 작성하며 API의 작동을 확인해야 했다 T_T

완성하고 나서 수행해야할 과제를 다시 확인해 보는데, 다다음주차 커리큘럼에 `ViewSet`이 있었다...!

![Screen Shot 2021-10-15 at 1 46 51 PM](https://user-images.githubusercontent.com/53527600/137433779-55cdc33b-0061-404f-aa3d-c74ca5b95576.png)

다다음주차에 배울 내용이기도 하고, 지금 까지의 이해도로는 `ViewSet` 적용이 큰 의미가 없는 것 같아서 다시 노션에 공유해 주셨던 view 함수 템플릿을 가져다 쓰는 식으로 리팩토링을 하기로 결정했다.

### 아쉬운 점
1. 이미지 처리 관련하여서 오류를 **상당히** 많이 겪어서 비디오 파일은 손도 못 댔는데, 다음에는 비디오 파일도 처리할 수 있으면 좋을 것 같다. 
2. 처음에는 Postman 작동이 생각하는 것 처럼 잘 안 돼서 별로라고 생각했는데, 내가 바보였을 뿐 Postman은 완전 짱이다! 이미지 파일 업로드 테스트 하는 부분에서 Postman 없었으면 큰일 날 뻔 했다. 사용법을 잘 읽어보고 했으면 삽질을 조금 덜 했을텐데... 다음 부터는 새로 접하는 툴은 무작정 해 보려고 하지 말고 **꼭** 사용법을 먼저 읽어봐야 겠다. 
