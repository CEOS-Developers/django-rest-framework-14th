from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, Post, Follow, File, Comment, Like
from .serializers import UserSerializer, ProfileSerializer, PostSerializer, FollowSerializer, FileSerializer, CommentSerializer, LikeSerializer

from .services.PostService import PostService

class UserList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

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