from rest_framework import serializers
from .models import Profile, Post, Media, Comment, Like

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'caption', 'created_at', 'updated_at', 'comments']

    def get_author(self, obj):
        return obj.author.username

    def get_comments(self, obj):
        queries = obj.post_comments.all()
        comments = []
        for query in queries:
            comment = {'author': query.author.username, 'content': query.content, 'created_at': query.created_at}
            comments.append(comment)
        return comments
