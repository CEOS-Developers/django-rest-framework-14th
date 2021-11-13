from django.http import Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from api.serializers import PostSerializer
from api.models import Post
from django.contrib.auth.models import User


class PostService():
    def getAllPost(self):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def getOnePostById(self, id):
        post = get_object_or_404(Post, pk=id)
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)

    def createPost(self, data):
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            temp_user = User.objects.get(id=data["user"])
            serializer.save(user=temp_user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def updatePost(self, data, id):
        post = get_object_or_404(Post, pk=id)
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def deletePost(self, id):
        post = get_object_or_404(Post, pk=id)
        post.delete()
        return Response({"message: delete success"}, )