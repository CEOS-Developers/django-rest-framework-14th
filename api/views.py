from rest_framework import viewsets
from api.models import Post, Profile
from api.serializers import PostSerializer, ProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet, filters


class PostFilter(FilterSet):
    content = filters.CharFilter(field_name='content')
    content_null = filters.BooleanFilter(field_name='content', method='is_content_null')

    class Meta:
        model = Post
        fields = '__all__'

    def is_content_null(self,queryset,content,value):
        if value:
            return queryset.filter(content__isnull=True)
        else:
            return queryset.filter(content__isnull=False)


class ProfileFilter(FilterSet):
    nickname = filters.CharFilter(field_name='nickname')

    class Meta:
        model = Profile
        fields =['nickname']


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = PostFilter


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()