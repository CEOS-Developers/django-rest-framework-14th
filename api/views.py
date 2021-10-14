from rest_framework import serializers, viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, Post, Photo, Video, Like, Comment, FollowRelation
from .serializers import ProfileSerializer, PostSerializer, PostDetailSerializer, CommentSerializer, LikeSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        post_serializers = {
            'list': PostSerializer,
            'detail': PostDetailSerializer,
        }
        if self.action == 'list':
            return post_serializers['list']
        if self.action == 'retrieve':
            return post_serializers['detail']
        else:
            return post_serializers['list']

    def create(self, request, *args, **kwargs):
        try:
            profile_id = request.data.get('profile_id')
            images_data = request.FILES.getlist('image_files')
            Post.objects.create(
                profile=Profile.objects.get(pk=profile_id),
                caption=request.data.get('caption')
            )
            for image_data in images_data:
                Photo.objects.create(post=post, image_file=image_data)
        except Exception:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            post_id = request.data.get('post_id')
            account_name = request.data.get('account_name')
            Comment.objects.create(
                post=Post.objects.get(pk=post_id),
                profile=Profile.objects.filter(account_name=account_name).first(),
                content=request.data.get('content')
            )
        except Exception:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
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
    
    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)
