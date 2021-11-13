from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Profile, Post, Photo, Video, Like, Comment, FollowRelation
from .serializers import ProfileSerializer, PostSerializer, PostDetailSerializer, CommentSerializer, LikeSerializer
from rest_framework.views import APIView


class PostList(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request, format=None):
        try:
            profile_id = request.data.get('profile_id')
            images_data = request.FILES.getlist('image_files')
            post = Post.objects.create(
                profile=Profile.objects.get(pk=profile_id),
                caption=request.data.get('caption')
            )
            for image_data in images_data:
                Photo.objects.create(post=post, image_file=image_data)
            serializer = PostDetailSerializer(post, many=False)
        except Exception:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status.HTTP_200_OK)


class PostDetail(APIView):
    def get(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        serializer = PostDetailSerializer(post, many=False)
        return JsonResponse(serializer.data, safe=False)
    
    def delete(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        serializer = PostDetailSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetail(APIView):
    def get(self, request, format=None):
        profile = Profile.objects.get(pk=profile_id)
        serializer = ProfileSerializer(profile, many=False)
        return JsonResponse(serializer.data, safe=False)


class CommentDetail(APIView):
    def post(self, request, format=None):
        try:
            post_id = request.data.get('post_id')
            account_name = request.data.get('account_name')
            comment = Comment.objects.create(
                post=Post.objects.get(pk=post_id),
                profile=Profile.objects.filter(account_name=account_name).first(),
                content=request.data.get('content')
            )
            serializer = CommentSerializer(comment, many=False)
        except Exception:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status.HTTP_200_OK)

    def get(self, request, format=None):
        profile = Comment.objects.get(pk=comment_id)
        serializer = CommentSerializer(profile, many=False)
        return JsonResponse(serializer.data, safe=False)


class LikeDetail(APIView):
    def post(self, request, format=None):
        try:
            post_id = request.data.get('post_id')
            account_name = request.data.get('account_name')
            like = Like.objects.create(
                post=Post.objects.get(pk=post_id),
                profile=Profile.objects.filter(account_name=account_name).first()
            )
            serializer = LikeSerializer(like, many=False)
        except Exception:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status.HTTP_200_OK)
