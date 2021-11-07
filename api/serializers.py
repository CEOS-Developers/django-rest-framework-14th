from rest_framework import serializers
from .models import *


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    writer_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['post', 'writer', 'content', 'created_at', 'updated_at', 'writer_nickname']


    def get_writer_nickname(self,obj):
        return obj.writer.nickname


class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField()
    post_like = LikeSerializer(many=True, read_only=True, source="like_set")
    post_comment = CommentSerializer(many=True, read_only=True, source="comment_set")
    
    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'author_nickname',
                  'created_at', 'updated_at', 'post_like', 'post_comment']

    def get_author_nickname(self, obj):
        return obj.author.nickname


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'nickname', 'introduction']