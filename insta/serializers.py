from rest_framework import serializers
from .models import Profile, Post, Comment, Follow, FollowRelation
from django.contrib.auth.models import User


class FolloweeListingField1(serializers.RelatedField):
    def to_representation(self, value):
        return value.follower.nickname


class FolloweeListingField2(serializers.RelatedField):
    def to_representation(self, value):
        return value.nickname


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.nickname # author의 값이 foreignkey로 pk인 id 값을 가져오기 때문에 nickname을 가져오도록 재정의

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'post']  # 정참조 시에는 그대로(author, post)


class PostSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True) # Nested Srializer를 이용해 relation을 맺은 다른 모델과의 관계 표현하기
    author = serializers.SerializerMethodField()

    def get_author(self, obj): # author의 값이 foreignkey로 pk인 id 값을 가져오기 때문에 nickname을 가져오도록 재정의
        return obj.author.nickname

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'comment_set']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProfileSerializer(serializers.ModelSerializer):
    post_set = PostSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    followee = FolloweeListingField1(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'nickname', 'user', 'followee', 'post_set'] # followee: 역참조


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField()
    followee = FolloweeListingField2(many=True, read_only=True)

    def get_follower(self, obj):
        return obj.follower.nickname

    class Meta:
        model = Follow
        fields = ['follower', 'followee']