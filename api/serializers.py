from rest_framework import serializers
from .models import *


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['follower', 'following']

    def get_follower(self, obj):
        return obj.follower.nickname

    def get_following(self, obj):
        return obj.following.nickname


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['author_name', 'author', 'post', 'content', 'created_date']

    def get_author_name(self, obj):
        return obj.author.nickname


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    post_likes = LikeSerializer(many=True, read_only=True)   # read_only: 요청 파라미터에 포함되지 않음.
    comments = CommentSerializer(many=True, read_only=True)
    post_files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['author_name', 'author', 'content', 'created_date', 'updated_date', 'comments_count', 'likes_count', 'post_likes', 'comments', 'post_files']

    def get_author_name(self, obj):
        return obj.author.nickname

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        return obj.post_likes.count()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'image', 'info', 'profile_name', ]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    posts = PostSerializer(many=True, read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)
    followers = FollowSerializer(many=True, read_only=True)
    followings = FollowSerializer(many=True, read_only=True)
    # likes = LikeSerializer(many=True, read_only=True)

    posts_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['nickname', 'username', 'password', 'email', 'profile', 'followers_count', 'followings_count', 'posts_count', 'posts', 'followers', 'followings']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def get_posts_count(self, obj):
        return obj.posts.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.followings.count()