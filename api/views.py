from .models import Post, User
from .serializers import PostSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from .filters import PostFilter, UserFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter


# class PostList(APIView):
#     """
#       View to List all posts, or create a new post.
#     """
#     def get(self, request, format=None):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class PostDetail(APIView):
#     """
#         View to detail post
#     """
#     def get_object(self, pk):
#         post = get_object_or_404(Post, pk=pk)
#         return post
#
#     def get(self, request, pk, format=None):
#         post = self.get_object(pk=pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         post = self.get_object(pk=pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         post = self.get_object(pk=pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class UserList(APIView):
#     def get(self, request, format=None):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class UserDetail(APIView):
#     def get_object(self, pk):
#         user = get_object_or_404(User, pk=pk)
#         return user
#
#     def get(self, request, pk, format=None):
#         user = self.get_object(pk=pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         user = self.get_object(pk=pk)
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         user = self.get_object(pk=pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


