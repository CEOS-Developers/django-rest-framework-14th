from rest_framework import serializers
from .models import *


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        field = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        field = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        field = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        field = ['content', 'created_date', 'get_user_nickname']

    def get_user_nickname(self, obj):
        return obj.user.nickname


class PostSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)  #read_only: 요청 파라미터에 포함되지 않음.
    comments = CommentSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'created_date', 'updated_date', 'author_id', 'likes', 'comments', 'files']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'info', 'profile_name', 'user_id']


class UserSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer(read_only=True)
    posts = PostSerializer(many=True, read_only=True)
    follower = FollowSerializer(many=True, read_only=True)
    following = FollowSerializer(many=True, read_only=True)
    # likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['nickname', 'username', 'password', 'email', 'posts', 'follower', 'following']