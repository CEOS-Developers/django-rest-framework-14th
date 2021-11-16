from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from .models import *
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    # /api/posts/reversed_id
    @action(detail=False)
    def reversedid(self, request):
        reversed_posts = Post.objects.all().order_by("-id")
        serializer = PostSerializer(reversed_posts, many=True)
        return Response(serializer.data)

    # /api/posts/1/customDetailFunction
    @action(detail=True)
    def customDetailFunction(self, request, pk=None):
        return Response({"data": "커스텀한 정보"})
