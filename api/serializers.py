from django.db.models import fields
from rest_framework import serializers
from .models import Profile, Post, Photo, Video, Like, Comment, FollowRelation


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'account_name', 'phone', 'bio', 'profile_photo']


class PostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'profile', 'caption', 'likes_count', 'comments_count', 'date_posted']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()
