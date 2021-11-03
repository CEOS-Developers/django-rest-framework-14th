from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'photo']


class UserSerializer(serializers.ModelSerializer):
    # OneToOne Relationship Serializer (Profile)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'profile', 'username', 'password', 'last_name', 'first_name', 'email']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'video', 'created_at', 'updated_at']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)
    post_likes = LikeSerializer(many=True, read_only=True)
    post_comments = CommentSerializer(many=True, read_only=True)
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'images', 'videos', 'post_likes', 'post_comments', 'created_at', 'updated_at', 'text']
