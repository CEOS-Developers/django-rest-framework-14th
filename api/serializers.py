from rest_framework import serializers
from .models import *


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['post', 'content']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post', 'user']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['post', 'writer', 'content']


class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField()
    post_like = LikeSerializer(many=True, read_only=True)
    post_comment = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'post_like', 'post_comment', 'author_nickname']

    def get_author_nickname(self, obj):
        return obj.author_nickname


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'nickname', 'introduction']