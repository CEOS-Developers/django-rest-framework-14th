from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, mixins, status

from .models import *
from .serializers import PostSerializer


class PostViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
