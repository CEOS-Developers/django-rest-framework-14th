from django.db.models import fields
from rest_framework import serializers
from .models import Profile, Post, Photo, Video, Like, Comment, FollowRelation


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'account_name', 'phone', 'bio', 'profile_photo']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image_file']


class PostSerializer(serializers.ModelSerializer):
    account_name = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'account_name', 'profile_photo', 'photos', 'caption', 'likes_count', 'comments_count', 'date_posted']

    def get_account_name(self, obj):
        return obj.profile.account_name

    def get_profile_photo(self, obj):
        return obj.profile.profile_photo

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    account_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'account_name', 'content']

    def get_account_name(self, obj):
        return obj.profile.account_name


class PostDetailSerializer(PostSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['comments']


class LikeSerializer(serializers.ModelSerializer):
    post_id = serializers.SerializerMethodField()
    account_name = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ['id', 'post_id', 'account_name']
    
    def get_account_name(self, obj):
        return obj.profile.account_name
