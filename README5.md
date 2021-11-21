## 6주차 DRF 과제

### 과제1. Viewset으로 리팩토링하기

```python
# User 모델
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = UserFilter


# Post 모델
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


# Follow 모델
class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
```

* ModelViewSet
> List, Create -> 전체 get, 새로 post 하는 것
> Retrieve, Destory, Update -> 해당하는 pk 관련하여 수정, 삭제


* GET, POST, PUT, PATCH, DELETE 모두 잘 돌아가는 것 확인 완료

```python
# 추가
from rest_framework import routers
from .views import PostViewSet, UserViewSet, FollowViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)
router.register(r'follows', FollowViewSet)

urlpatterns = router.urls
```

* Routers
> 몇몇의 web framework들은 들어오는 request를 핸들링하여 logic과 어플리케이션을 위한 URL을 어떻게 매핑할지를 자동으로 결정하는 기능을 제공한다.
> REST framework는 장고에 자동적인 URL 라우팅 기능을 지원하고 신속하고 일관성 있는 방법을 제공한다.

* register() method
> register() method는 2개의 필수 argument를 필요로 한다.
>>*  prefix - router의 집합들을 사용하기 위한 URL prefix   
>>*  viewset - viewset 클래스



### 2. filter 기능 구현하기

```python
# User Filter 추가 -> 성별을 기준으로 필터링하기
class UserFilter(FilterSet):
    gender = filters.CharFilter(method='filter_gender')

    def filter_gender(self, queryset, name, value):
        filtered_queryset = queryset.filter(gender=value)
        return filtered_queryset

    class Meta:
        model = User
        fields = ['gender']


# User 모델
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = UserFilter
```

처음에 user 전체를 조회했을 때는
```json
[
    {
        "id": 1,
        "username": "superuser",
        "email": "sssssjin99@naver.com",
        "gender": "female",
        "created_at": "2021-11-19T09:56:41.804207",
        "updated_at": "2021-11-19T10:13:29.530670"
    },
    {
        "id": 2,
        "username": "user2",
        "email": "user2@naver.com",
        "gender": "male",
        "created_at": "2021-11-19T10:12:13.032984",
        "updated_at": "2021-11-19T10:13:19.931225"
    },
    {
        "id": 3,
        "username": "user3",
        "email": "user3@naver.com",
        "gender": "male",
        "created_at": "2021-11-19T10:12:48.874004",
        "updated_at": "2021-11-19T10:13:00.183623"
    },
    {
        "id": 4,
        "username": "user4",
        "email": "user4@naver.com",
        "gender": "female",
        "created_at": "2021-11-19T10:13:52.839179",
        "updated_at": "2021-11-19T10:13:52.839179"
    },
    {
        "id": 5,
        "username": "user5",
        "email": "user5@naver.com",
        "gender": "female",
        "created_at": "2021-11-19T10:14:20.788760",
        "updated_at": "2021-11-19T10:14:20.788760"
    },
    {
        "id": 6,
        "username": "user6",
        "email": "user6@naver.com",
        "gender": "male",
        "created_at": "2021-11-19T10:16:00.381504",
        "updated_at": "2021-11-19T10:16:00.381504"
    }
]
```

이었는데, 여기에 filter에 성별을 male만 걸어서 가져왔을 때에는

```json
[
    {
        "id": 2,
        "username": "user2",
        "email": "user2@naver.com",
        "gender": "male",
        "created_at": "2021-11-19T10:12:13.032984",
        "updated_at": "2021-11-19T10:13:19.931225"
    },
    {
        "id": 3,
        "username": "user3",
        "email": "user3@naver.com",
        "gender": "male",
        "created_at": "2021-11-19T10:12:48.874004",
        "updated_at": "2021-11-19T10:13:00.183623"
    },
    {
        "id": 6,
        "username": "user6",
        "email": "user6@naver.com",
        "gender": "male",
        "created_at": "2021-11-19T10:16:00.381504",
        "updated_at": "2021-11-19T10:16:00.381504"
    }
]
```

성별이 male인 자료만 잘 가져왔음을 확인할 수 있었습니다.


### 배운점 & 회고

viewSet을 처음 접하고 배워봤는데, 일단은 처음에는 정말 신세계였다. 내가 각각의 method에 따라서 달리 짠 이 많은 코드들을 단 몇줄에 나타낼 수 있다는 것이 정말 놀라웠다.   
그러면서도 한편, 이 viewSet의 내부에서 어떻게 잘 돌아가는지 알고 있어야 이를 능숙하게 이용할 수 있을 것 같았다.   
일단 너무 많이 간략화가 되어있기에, 이 viewSet을 배우기 전에 먼저 했었던 django view 부터 시작해서 rest_framework APIView 그리고 Generic Views까지   
이 것을 모두 공부한뒤에 viewSet을 접했기에 어느정도 viewSet이 이렇게 돌아가는지 알 수 있었던 것 같다.   
처음부터 viewSet을 접했다면 매우 혼란스럽지않았을까 싶었다.

* django view -> rest_framework APIView -> Generic Views


* viewsets 클래스와 view 클래스 비교
>* 반복되는 로직은 단일 클래스 안에 결합될 수가 있다, 그래서 viewset을 사용했을 때 queryset을 단 한번만 정의하면 되지만, view는 다수의 view들을 사용해야 한다.   
>* 라우터를 사용함으로써 더이상 URL 설정파일을 다루지 않아도 된다.   
>* 전체 프로젝트 내에 일관된 URL 구성을 적용할 수 있다.   

(단점은 아니지만 view가 더 좋은 점)
>*  기본 view와 URL 설정을 사용하면 더 명확해지고 상세한 제어를 할 수 있다.



>*  필요에 맞게, 상황에 맞게 유연하게 적절한 것을 골라쓰고 커스터마이징 하는 것이 가장 중요한 것이 아닐까 싶다.   
>*  그러기 위해서는 각각의 기능이 어떤 과정으로 이루어지고 돌아가는지 그 과정을 잘 공부해야한다고 생각한다!!