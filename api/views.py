from .models import Profile, Post, Photo, Video, Like, Comment, FollowRelation
from .serializers import ProfileSerializer, PostSerializer, PostDetailSerializer, CommentSerializer, LikeSerializer
from rest_framework import viewsets


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostDetailSerializer
    serializer_action_classes = {
        'list': PostSerializer,
    }
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
