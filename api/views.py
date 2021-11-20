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

    # create() 재정의
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
