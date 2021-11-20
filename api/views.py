from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Post, Profile
from api.serializers import PostSerializer, ProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet, filters


class PostFilter(FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr="icontains")#해당 문자열을 포함하는 queryset
    content_null = filters.BooleanFilter(field_name='content', method='is_content_null')

    class Meta:
        model = Post
        fields = ['content', 'title']

    def is_content_null(self, queryset,content, value):
        if value:
            return queryset.filter(content__isnull=True)
        else:
            return queryset.filter(content__isnull=False)


class ProfileFilter(FilterSet):
    nickname = filters.CharFilter(field_name='nickname')

    class Meta:
        model = Profile
        fields = ['nickname']


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = PostFilter


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = ProfileFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

