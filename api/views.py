from django.http.response import Http404
from rest_framework.utils import serializer_helpers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import PostSerializer


# /post
class PostList(APIView):
    # 게시물 목록 조회
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 게시물 생성
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():  # 데이터가 유효할 경우
            # (임시) user1이 작성한 게시물인 것으로 저장
            # 추후에는 현재 로그인한 유저정보를 request.user로 받아와서 저장하면 됨
            temp_user = User.objects.get(id=1)
            serializer.save(user=temp_user)  # 요청받은 데이터 저장
            # status 201 created
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /post/<pk>
class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format="json"):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
