## 5주차 과제

### 모든 list를 가져오는 API

- URL: `/api/posts/`
- Method: `GET`

```json
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

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
                "created_at": "2021-10-14T16:06:19.338340Z"
            },
            {
                "author": "ceos",
                "content": "HI",
                "created_at": "2021-10-14T16:07:27.006207Z"
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
                "created_at": "2021-10-14T16:06:31.398977Z"
            }
        ]
    },
    {
        "id": 19,
        "author": "user3",
        "caption": "포스트333",
        "created_at": "2021-10-15T00:16:26.793209+09:00",
        "updated_at": "2021-10-15T00:16:26.793209+09:00",
        "comments": []
    }
]
```

### 특정 데이터를 가져오는 API

- URL: `/api/posts/19/`
- Method: `GET`

```json
HTTP 200 OK
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 19,
    "author": "user3",
    "caption": "포스트333",
    "created_at": "2021-10-15T00:16:26.793209+09:00",
    "updated_at": "2021-10-15T00:16:26.793209+09:00",
    "comments": []
}
```

### 새로운 데이터를 생성하는 API

- URL: `/api/posts/`
- Method: `POST`
- Body: `{ "caption": "새로운 포스트!!!" }`

```json
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 25,
    "author": "user1",
    "caption": "새로운 포스트!!!",
    "created_at": "2021-11-11T02:50:15.233088+09:00",
    "updated_at": "2021-11-11T02:50:15.233088+09:00",
    "comments": []
}
```

### 특정 데이터를 업데이트하는 API

- URL: `/api/posts/25/`
- Method: `PUT`
- Body: `{ "caption": "수정 완료!" }`

```json
HTTP 200 OK
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 25,
    "author": "user1",
    "caption": "수정 완료!",
    "created_at": "2021-11-11T02:50:15.233088+09:00",
    "updated_at": "2021-11-11T02:52:33.863899+09:00",
    "comments": []
}
```

### 특정 데이터를 삭제하는 API

- URL: `/api/posts/25/`
- Method: `DELETE`

```json
HTTP 204 No Content
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
```

### APIView class란?

DRF의 APIView 클래스는 Django의 View 클래스의 서브클래스이고, DRF의 가장 기본적인 view class이다. APIView의 사용법은 장고의 View class와 비슷하다. HTTP method에 따라 handler method(`.get()`, `.post()`, ...)를 정의해서 request를 처리한다.

### 회고

개인적으로 FBV보단 CBV가 훨씬 코드도 깔끔하고 편하게 느껴진다. 하지만 특정 에러를 핸들링할 때는 CBV를 사용하지 않는 등 CBV가 FBV를 모든 부분에서 대체하지는 못한다고 하니 아쉽다. 왜 CBV를 사용하지 못하고 FBV를 사용해야만 하는지 더 공부해야 겠다.