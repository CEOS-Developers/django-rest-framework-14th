from .models import *
from .serializers import PostSerializer
from rest_framework import viewsets, mixins
from django_filters.rest_framework import filters, FilterSet
from django_filters.rest_framework import DjangoFilterBackend


class PostFilter(FilterSet):
    post_author = filters.CharFilter(field_name='author')

    class Meta:
        model = Post
        fields = ['location',]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter
