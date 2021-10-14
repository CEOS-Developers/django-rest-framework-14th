from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'private']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    like_username_list = serializers.SerializerMethodField()
    post_comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'author', 'like_username_list',
                  'post_comments', 'created_at', 'updated_at', ]

    def get_author(self, obj):  # 작성자 username 반환
        return obj.user.username

    # 게시글에 좋아요 누른 사용자의 username만을 받아와서 리스트로 저장
    def get_like_username_list(self, obj):
        return [like.user.username for like in obj.post_likes.all().select_related('user')]
