## 5주차 과제
### 모든 list를 가져오는 API
- URI: `/api/posts/`
- Method: `GET`
![Screen Shot 2021-11-13 at 1 12 06 AM](https://user-images.githubusercontent.com/53527600/141498714-28855fdc-279e-446e-88ab-e4c062fa2511.png)
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
        "comments_count": 1,
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
        "caption": "포스틱 포스트 포스트",
        "likes_count": 4,
        "comments_count": 2,
        "date_posted": "2021-10-15T13:08:49.525477+09:00"
    }
]
```

### 특정 데이터를 가져오는 API
- URI: `/api/post/5/`
- Method: `GET`
![Screen Shot 2021-11-13 at 1 16 27 AM](https://user-images.githubusercontent.com/53527600/141498913-1994607c-6146-4db1-ba22-9a4c531bc4d3.png)
```JSON
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
    "caption": "포스틱 포스트 포스트",
    "likes_count": 4,
    "comments_count": 2,
    "date_posted": "2021-10-15T13:08:49.525477+09:00",
    "comments": [
        {
            "id": 1,
            "post_id": 5,
            "account_name": "admin_profile",
            "profile_photo": "profiles/tmp4et5jeut.jpg",
            "content": "포스틱 맛있겠네요ㅎ"
        },
        {
            "id": 2,
            "post_id": 5,
            "account_name": "test0",
            "profile_photo": "profiles/tmp4et5jeut.jpg",
            "content": "감자튀김이 더 맛있음ㅋ"
        }
    ]
}
```

### 새로운 데이터를 생성하는 API
- URI: `/api/posts/`
- Method: `POST`
- 요청 시 body에 들어가야 하는 필드
  - profile_id: int
  - image_files: file(image)
  - caption: string 
![Screen Shot 2021-11-13 at 1 24 23 AM](https://user-images.githubusercontent.com/53527600/141500071-8d34c91c-992d-4807-b711-79271bedcd88.png)
```JSON
{
    "id": 6,
    "account_name": "test0",
    "profile_photo": "profiles/tmp4et5jeut.jpg",
    "photos": [
        {
            "id": 13,
            "image_file": "/media/posts/photos/Screen_Shot_2021-11-11_at_3.55.30_PM.png"
        }
    ],
    "caption": "샤인머스캣",
    "likes_count": 0,
    "comments_count": 0,
    "date_posted": "2021-11-13T01:24:18.939847+09:00",
    "comments": []
}
```

### 특정 데이터를 업데이트하는 API
- URI: `/api/post/5/`
- Method: `PATCH`
![Screen Shot 2021-11-13 at 1 19 04 AM](https://user-images.githubusercontent.com/53527600/141499300-2cc04601-e0c0-42a1-93fb-167115684b46.png)
```JSON
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
    "caption": "포스틱 포스트를 PATCH로 수정했어요~!",
    "likes_count": 4,
    "comments_count": 2,
    "date_posted": "2021-10-15T13:08:49.525477+09:00",
    "comments": [
        {
            "id": 1,
            "post_id": 5,
            "account_name": "admin_profile",
            "profile_photo": "profiles/tmp4et5jeut.jpg",
            "content": "포스틱 맛있겠네요ㅎ"
        },
        {
            "id": 2,
            "post_id": 5,
            "account_name": "test0",
            "profile_photo": "profiles/tmp4et5jeut.jpg",
            "content": "감자튀김이 더 맛있음ㅋ"
        }
    ]
}
```

### 특정 데이터를 삭제하는 API
- URI: `/api/post/3/`
- Method: `DELETE`
![Screen Shot 2021-11-13 at 1 28 10 AM](https://user-images.githubusercontent.com/53527600/141500644-cde515a5-5d8f-41e7-bbc0-093fe35688c0.png)
아래와 같이 status code 값이 204라서 반환값은 딱히 없다.
```Python
def delete(self, request, pk, format=None):
    post = Post.objects.get(pk=pk)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
```

`DELETE /api/post/3/` 요청 후 전체 Post list를 조회한 결과는 다음과 같다. id가 3인 post가 사라졌음을 알 수 있다. 
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
        "comments_count": 1,
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
        "caption": "포스틱 포스트를 PATCH로 수정했어요~!",
        "likes_count": 4,
        "comments_count": 2,
        "date_posted": "2021-10-15T13:08:49.525477+09:00"
    },
    {
        "id": 6,
        "account_name": "test0",
        "profile_photo": "profiles/tmp4et5jeut.jpg",
        "photos": [
            {
                "id": 13,
                "image_file": "/media/posts/photos/Screen_Shot_2021-11-11_at_3.55.30_PM.png"
            }
        ],
        "caption": "샤인머스캣",
        "likes_count": 0,
        "comments_count": 0,
        "date_posted": "2021-11-13T01:24:18.939847+09:00"
    }
]
```

### 공부한 내용 정리
HTTP Method 중 `PUT, PATCH` 는 모두 업데이트, 즉 데이터의 수정을 위해 쓰인다.
데이터를 업데이트 하는 API를 구현할 때 어떤 메서드를 사용해야 하나 고민을 하다가, 두 메서드의 차이점을 검색해보게 되었다. 

두 메서드의 정의를 간단히 각각 정리하면 다음과 같다. 

- `PUT`: 리소스를 대체한다. 
- `PATCH`: 리소스의 일부분을 수정한다.

`PUT` 요청 시 요청을 일부분만 보낼 경우 나머지는 디폴트 값으로 수정 되는 것이 원칙이다. 따라서 변경되는 점이 없는 속성까지도 모두 값을 담아 요청을 보내야 한다. 여기서 중요한 것은 만약 **일부분만 보낼 경우 전달한 필드 외의 나머지 필드는 모두 null 또는 default 값이 들어가 버린다** 는 것이다. 수정을 원치 않았던 부분이 수정되어 버릴 수도 있다는 의미이므로, `PUT` 요청을 보낼 시에는 반드시 수정을 원하는 필드 외에 다른 필드 또한 원래의 값을 채워 보내야 한다.

반면 `PATCH` 는 태생부터 데이터의 일부만 수정하기 위한 것으로, 수정하고 싶은 필드의 데이터만 담아 요청을 보내도 수정되지 않는 나머지 필드는 기존의 데이터가 유지된다. 

인스타그램 특성 상 `PATCH`를 사용하는 것이 더 적합할 것이라고 판단하여 `PATCH` 메서드를 사용하게 되었다.

### 간단한 회고
학교 기말고사 전 마지막 과제 기간과 겹쳐서 시간 안에 과제를 제출하지 못했다. 정신줄 놓고 과제를 까맣게 잊고 살다가 오늘까지 였던 학교 과제를 제출한 뒤에 긴장이 풀어진 채 쉬고 있었는데 코드 리뷰어인 민아님께 연락을 받았다... 민아님 아니었으면 제출이 더 늦어질 뻔했다. 일정을 관리하는 습관을 진짜 제발 제대로 들여야겠다는 생각을 했다. 정말 감사합니다 민아님ㅠㅠ🥺🥰
