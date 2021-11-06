from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'gender', 'phone_num', 'introduction', 'website']

class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['comment', 'nickname','created_date']

    def get_nickname(self,obj):
        return obj.user.nickname

class LikeSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ['nickname']

    def get_nickname(self,obj):
        return obj.user.nickname

class PostSerializer(serializers.ModelSerializer):
    post_likes = LikeSerializer(many=True,read_only=True)
    post_comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'author', 'location', 'title', 'post_likes', 'post_comments', 'created_date', 'updated_date']

    def to_representation(self, instance):
        self.fields['author'] = UserSerializer(read_only=True)
        return super(PostSerializer,self).to_representation(instance)

