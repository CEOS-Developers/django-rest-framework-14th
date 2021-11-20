from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    post_author = serializers.SerializerMethodField()
    post_comments = CommentSerializer(many=True, read_only=True)

    def get_post_author(self, obj):
        return obj.post_author.username

    class Meta:
        model = Post
        fields = ['id', 'post_author', 'post_content', 'post_comments', 'location']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'instagram_id', 'is_professional']


