from rest_framework import serializers
from .models import Profile, Post, File, Comment, Like, Follow
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id',
                  'username',
                  'firstName',
                  'lastName',
                  'picture',
                  'createdAt',
                  'updatedAt',
                  'deletedAt',
                  'isDeleted',
                  ]

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id',
                  'url',
                  'createdAt',
                  'updatedAt',
                  'deletedAt',
                  'isDeleted',
                  ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id',
                  'text',
                  'createdAt',
                  'updatedAt',
                  'deletedAt',
                  'isDeleted',
                  ]

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id',
                  'createdAt',
                  'updatedAt',
                  'deletedAt',
                  'isDeleted',
                  ]

class PostSerializer(serializers.ModelSerializer):
    files = FileSerializer(source='file_set', many=True, read_only=True)
    comments = CommentSerializer(source='comment_set', many=True, read_only=True)
    likes = LikeSerializer(source='like_set', many=True, read_only=True)

    # Serializer Method Field
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'id',
            'caption',
            'location',
            'like_count',
            'comment_count',
            'comments',
            'files',
            'likes',
            'createdAt',
            'updatedAt',
            'deletedAt',
            'isDeleted',
        ]

    def get_like_count(self, obj):
        return obj.like_set.count()

    def get_comment_count(self, obj):
        return obj.comment_set.count()

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id',
                  'createdAt',
                  'updatedAt',
                  'deletedAt',
                  'isDeleted',
                  ]

class UserSerializer(serializers.ModelSerializer):
    # OneToOne Relationship Searialzer (Profile)
    firstName = serializers.CharField(source='profile.firstName', read_only=True)
    lastName = serializers.CharField(source='profile.lastName', read_only=True)
    picture = serializers.CharField(source='profile.picture', read_only=True)
    createdAt = serializers.CharField(source='profile.createdAt', read_only=True)
    updatedAt = serializers.CharField(source='profile.updatedAt', read_only=True)
    deletedAt = serializers.CharField(source='profile.deletedAt', read_only=True)
    isDeleted = serializers.CharField(source='profile.isDeleted', read_only=True)

    # Nested Serailzer
    posts = PostSerializer(source='post_set', many=True, read_only=True)
    comments = CommentSerializer(source='comment_set', many=True, read_only=True)
    likes = LikeSerializer(source='like_set', many=True, read_only=True)

    # Serializer Method Field
    follower_number = serializers.SerializerMethodField()
    followee_number = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id',
                  'email',
                  'password',
                  'follower_number',
                  'followee_number',
                  'username',
                  'firstName',
                  'lastName',
                  'picture',
                  'createdAt',
                  'updatedAt',
                  'deletedAt',
                  'isDeleted',
                  'posts',
                  'comments',
                  'likes',
                  ]

    def get_follower_number(self, obj):
        return obj.followee_user.count()

    def get_followee_number(self, obj):
        return obj.follower_user.count()