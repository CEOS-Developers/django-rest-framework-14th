from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = {'id', 'username', 'nickname', 'gender', 'phone_num', 'introduction', 'website'}

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    like_users = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = {'id', 'user', 'location', 'title', 'like_users', 'commnets', 'created_at', 'updated_at'}

    def get_author(self, obj):
        return obj.user.username

    def get_comment_list(self, obj):
        return self.comments