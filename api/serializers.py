from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'gender', 'phone_num', 'introduction', 'website']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment', 'user','created_date']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user','created_date']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    post_likes = LikeSerializer(many=True,read_only=True)
    post_comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'author', 'location', 'title', 'post_likes', 'post_comments', 'created_date', 'updated_date']

    def get_author(self, obj):
        return obj.author.nickname
