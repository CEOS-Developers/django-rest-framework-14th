from django.shortcuts import render, redirect
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer, PostSerializer, FollowSerializer, ProfileSerializer

from .models import Profile, Post, Follow
from django.contrib.auth.models import User


# Post 모델
# 1. 전체 Post 가져오기
@api_view(['GET'])
def postList(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)


# 2. 한 개의 Post 가져오기
@api_view(['GET'])
def postDetail(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post)

    return Response(serializer.data)


# Profile 모델
# 1. 전체 Profile 가져오기
@api_view(['GET'])
def profileList(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)

    return Response(serializer.data)


# 2. 한 명의 Profile 가져오기
@api_view(['GET'])
def profileDetail(request, pk):
    profile = Profile.objects.get(id=pk)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)


# 3. Profile 생성하기
@api_view(['POST'])
def profileCreate(request):
    data = JSONParser().parse(request)
    serializer = ProfileSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


# Follow 모델
# 1. 전체 팔로우 관계 조회하기
@api_view(['GET'])
def followList(request):
    follows = Follow.objects.all()
    serializer = FollowSerializer(follows, many=True)

    return Response(serializer.data)


# 2. 특정 유저의 팔로우 관계 조회하기
@api_view(['GET'])
def followDetail(request, pk):
    follow = Follow.objects.get(follower=pk)  # get: 객체반환, filter: 쿼리셋(객체 여러개)를 반환
    print(follow)
    serializer = FollowSerializer(follow)

    return Response(serializer.data)