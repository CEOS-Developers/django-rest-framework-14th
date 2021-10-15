from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Profile, Post, Photo, Video, Like, Comment, FollowRelation
from .serializers import ProfileSerializer, PostSerializer, PostDetailSerializer, CommentSerializer, LikeSerializer


@csrf_exempt
@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
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


@csrf_exempt
@api_view(['GET'])
def post_detail(request, post_id):
    if request.method == 'GET':
        post = Post.objects.get(pk=post_id)
        serializer = PostDetailSerializer(post, many=False)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(['GET'])
def profile_detail(request, profile_id):
    if request.method == 'GET':
        profile = Profile.objects.get(pk=profile_id)
        serializer = ProfileSerializer(profile, many=False)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(['POST'])
def comment_create(request):
    if request.method == 'POST':
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


@csrf_exempt
@api_view(['GET'])
def comment_detail(request, comment_id):
    if request.method == 'GET':
        profile = Comment.objects.get(pk=comment_id)
        serializer = CommentSerializer(profile, many=False)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(['POST'])
def like_create(request):
    if request.method == 'POST':
        try:
            post_id = request.data.get('post_id')
            account_name = request.data.get('account_name')
            Like.objects.create(
                post=Post.objects.get(pk=post_id),
                profile=Profile.objects.filter(account_name=account_name).first()
            )
        except Exception:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status.HTTP_200_OK)
