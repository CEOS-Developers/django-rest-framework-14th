from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, Post, Follow, File, Comment, Like
from .serializers import UserSerializer, ProfileSerializer, PostSerializer, FollowSerializer, FileSerializer, CommentSerializer, LikeSerializer

from .services.PostService import PostService

# 6주차 DRF
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters
#from rest_framework import filters


'''
class UserList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
'''

class UserFilter(FilterSet):
    username = filters.CharFilter(field_name='username')
    lastName = filters.CharFilter(method='filter_lastName')

    def filter_lastName(self, queryset, name, value):
        filtered_queryset = queryset.filter(profile__lastName__startswith=value)
        return filtered_queryset

    class Meta:
        model = User
        fields = ['username']



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = Post.objects.all()
        location = self.request.query_params.get('location')
        if location is not None:
            queryset = queryset.filter(location=location)
        return queryset


'''
class PostList(APIView):
    def get(self, request, format=None):
        return PostService().getAllPost()

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        return PostService().createPost(data)


class PostDetail(APIView):
    def get(self, request, id, format=None):
        return PostService().getOnePostById(id)

    def put(self, request, id, format=None):
        data = JSONParser().parse(request)
        return PostService().updatePost(data, id)

    def delete(self, request, id, format=None):
        return PostService().deletePost(id)
    '''