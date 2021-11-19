from rest_framework import serializers
from .models import User, Post, Comment, Follow


# Viewset을 위해 새로 추가
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'author', 'content']
##


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField() # serializer method field 이용

    def get_author(self, obj):
        return obj.author.username # author의 값이 foreignkey로 pk인 id 값을 가져오기 때문에 nickname을 가져오도록 재정의

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'post']  # 정참조 시에는 그대로(author, post)


class PostListSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True) # Nested Serializer를 이용해 relation을 맺은 다른 모델과의 관계 표현하기
    author = serializers.SerializerMethodField() # serializer method field 이용

    def get_author(self, obj): # author의 값이 foreignkey로 pk인 id 값을 가져오기 때문에 username을 가져오도록 재정의
        return obj.author.username

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'comment_set']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'content']


## User 모델
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'gender', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


## Follow 모델
# 팔로우-팔로잉 전체 관계 조회 serializer
class FollowSerializer(serializers.ModelSerializer):
    userFrom = serializers.SerializerMethodField()
    userTo = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['id', 'userFrom', 'userTo']

    def get_userFrom(self, obj):
        return obj.userFrom.username
    def get_userTo(self, obj):
        return obj.userTo.username


# 특정 유저의 팔로잉 serializer
class FollowingSerializer(serializers.ModelSerializer):
    userTo = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['userTo']

    def get_userTo(self, obj):
        return obj.userTo.username


# 특정 유저의 팔로우 serializer
class FolloweeSerializer(serializers.ModelSerializer):
    userFrom = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['userFrom']

    def get_userFrom(self, obj):
        return obj.userFrom.username


# class FolloweeListingField1(serializers.RelatedField):
#    def to_representation(self, value):
#       return value.follower.nickname
#
#
# class ProfileListSerializer(serializers.ModelSerializer):
#     post_set = PostListSerializer(many=True, read_only=True)
#     user = UserSerializer(read_only=True)
#     followee = FolloweeListingField1(many=True, read_only=True) # many to many 관계 모델 기져오기
#
#     class Meta:
#         model = Profile
#         fields = ['id', 'nickname', 'user', 'followee', 'post_set'] # followee: 역참조
#
#
# class ProfilePartSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#
#     class Meta:
#         model = Profile
#         fields = ['id', 'nickname', 'user']
#
#
# class FolloweeListingField2(serializers.RelatedField):
#     def to_representation(self, value):
#         return value.nickname
#
#
# class FollowSerializer(serializers.ModelSerializer):
#     follower = serializers.SerializerMethodField()
#     followee = FolloweeListingField2(many=True, read_only=True)
#
#     def get_follower(self, obj):
#         return obj.follower.nickname
#
#     class Meta:
#         model = Follow
#         fields = ['follower', 'followee']