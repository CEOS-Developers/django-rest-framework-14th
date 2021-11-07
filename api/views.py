from .models import Post
from .serializers import PostSerializer
from rest_framework import viewsets


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # create() 재정의
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
