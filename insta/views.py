from django.shortcuts import render, redirect
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer, UserCreateSerializer, PostListSerializer, PostCreateSerializer, PostSerializer
from .serializers import FollowSerializer, FollowingSerializer, FolloweeSerializer

from .models import User, Post, Follow

## 추가
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
import django_filters.rest_framework
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions


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


# Post 모델
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


# Follow 모델
class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()


# # Post 모델
# # 1. 전체 Post 가져오기 or # 2. 새 Post 작성하기
# class postList(APIView):
#     def get(self, request, format=None):
#         posts = Post.objects.all()
#         serializer = PostListSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = PostCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
#
#
# # 3. 특정 Post 가져오기 or # 4. 특정 포스트 수정하기 # 5. 특정 포스트 삭제하기
# class postDetail(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(Post, id=pk)
#
#     def get(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostListSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostCreateSerializer(post, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
#
#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=201)
#
#
# # User 모델
# # 1. 전체 User 가져오기 or # 2. 새 User 추가하기
# class userList(APIView):
#
#     def get(self, request, format=None):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         #print(request.data["username"])
#         #print(request.data["email"])
#         # username / email에 대한 예외 처리 추가할 것
#         serializer = UserCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
#
#
#
#
# # 3. 특정 User 가져오기 or # 4. 특정 User 수정하기 # 5. 특정 User 삭제하기
# class userDetail(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(User, id=pk)
#
#     def get(self, request, pk, format=None):
#         user = User.objects.get(id=pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         user = self.get_object(pk)
#         serializer = UserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#
#     def delete(self, request, pk):
#         user = User.objects.get(id=pk)
#         user.delete()
#         return Response(status=204)
#
#
# # Follow 모델
# # 1. 전체 팔로우 관계 조회하기
# class followList(APIView):
#     def get(self, request, format=None):
#         follows = Follow.objects.all()
#         serializer = FollowSerializer(follows, many=True)
#         return Response(serializer.data)
#
#
# # 2. 특정 유저가 팔로잉하는 유저(들) 조회하기
# class following(APIView):
#     def get(self, request, pk, format=None):
#         userFrom = User.objects.get(id=pk)
#         queryset = Follow.objects.filter(userFrom=userFrom)
#         serializer = FollowingSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#
# # 3. 특정 유저를 팔로우하는 유저(들) 조회하기
# class followee(APIView):
#     def get(self, request, pk, format=None):
#         userTo = User.objects.get(id=pk)
#         queryset = Follow.objects.filter(userTo=userTo)
#         serializer = FolloweeSerializer(queryset, many=True)
#         return Response(serializer.data)