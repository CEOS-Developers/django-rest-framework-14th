# 6주차 DRF3: ViewSet Filter Permission Validation

## ViewSet

ViewSet은 말그대로 views의 모음이다. ViewSet을 사용하면 관련된 views를 하나의 class로 결합할 수 있다. 

- `views.py`

```python
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

기존의 APIView를 ModelViewSet을 사용해 리팩토링했다. 포스트를 생성할 때는 author의 정보가 필요하기 때문에 유저 정보를 넘겨주기 위해 `create()` 만 재정의하였다.

- `urls.py`

```python
from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls))
]
```

APIView를 사용했을 때는 하나의 뷰를 하나의 url pattern에 연결했다. ViewSet은 router를 사용해 자동으로 여러 개의 url pattern을 처리하는 것이 좋다고 한다.

## FilterSet

FilterSet은 기본적으로 url의 query parameter를 분석하여 쿼리셋을 자동 필터링해준다.

문자열의 단순한 일치 여부만 확인하는 필터라면 간편하게 ViewSet에 `filterset_fields` 를 적어주면 된다. 그 외의 필터링을 정의하고 싶다면, FilterSet class를 상속받아 구현한 후 ViewSet에 `filterset_class` 에 넣어준다. (`filterset_fields` 와 `filterset_class` 는 동시에 사용할 수 없음)

- `views.py`

```python
from .models import Post
from .serializers import PostSerializer
from rest_framework import viewsets
from django_filters import rest_framework as filters

class PostFilter(filters.FilterSet):
    author = filters.CharFilter(method='filter_author')

    class Meta:
        model = Post
        fields = {
            # caption에 특정 내용이 포함되는 포스트만 필터링
            'caption': ['exact', 'icontains'],
        }

    # username으로 특정 유저의 포스트만 필터링
    def filter_author(self, queryset, name, value):
        username = '__'.join([name, 'username', 'iexact'])
        return queryset.filter(**{
            username: value
        })

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

2가지 필터 기능을 구현하였다.

1. caption에 특정 내용이 포함된(혹은 특정 내용과 일치하는) 포스트만 필터링
2. 특정 username을 가진 유저가 작성한 포스트만 필터링

caption 필터링은 FilterSet의 `Meta.fields` 를 이용하여 아주 간략하게 구현하였다. caption이 value와 정확히 일치하거나 caption에 value가 포함되어 있는(대소문자 구분 없이) 포스트만 가져온다.

username 필터링은 method를 정의해서 구현하였다. username이 value와 일치하는(대소문자 구분 없이) 사용자가 작성한 포스트만 가져온다.

### 결과

- Method: `GET`
- url: `/api/posts/?caption__icontains=new&author=user1`

```json
HTTP 200 OKAllow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 26,
        "author": "user1",
        "caption": "new",
        "created_at": "2021-11-17T16:39:07.925765+09:00",
        "updated_at": "2021-11-17T16:39:07.925765+09:00",
        "comments": []
    },
    {
        "id": 27,
        "author": "user1",
        "caption": "새로운 포스트 new post",
        "created_at": "2021-11-18T19:11:04.917265+09:00",
        "updated_at": "2021-11-18T19:11:04.925428+09:00",
        "comments": []
    }
]
```

- 에러

![에러](https://user-images.githubusercontent.com/71026706/142432142-7a81033e-eaa4-47c5-a611-0158b64e4802.png)

```python
class PostViewSet(viewsets.ModelViewSet):
    ...
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PostFilter
```

여기서 `filters.DjangoFilterBackend` 를 리스트에 넣어주지 않았더니 이러한 에러가 발생하였다. Alt+Shift+Enter를 생각 없이 누르지 말아야겠다..🙃
