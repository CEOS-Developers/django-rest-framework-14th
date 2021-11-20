from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from rest_framework import status,generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

import django_filters
from django_filters.rest_framework import DjangoFilterBackend,filters,FilterSet
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *

class PostFilter(FilterSet):
    author = filters.NumberFilter(field_name='author')
    author__gt = filters.NumberFilter(field_name='author', lookup_expr='gt')
    location = filters.CharFilter(field_name='location')

    class Meta:
        model = Post
        fields = ['author', 'location']


class UserFilter(FilterSet):
    username = filters.CharFilter(field_name='username')
    nickname = filters.CharFilter(field_name='nickname')

    class Meta:
        model = User
        fields = ['username', 'nickname']


class PostViewSet(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend,]
    filter_class = PostFilter

    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(author=self.request.user)
    # filterset_fields = ['author', 'location']
    '''
    def get_queryset(self):
        queryset = Post.objects.all()
        authorname = self.request.query_params.get('author')
        if authorname is not None:
            queryset = queryset.filter(author=authorname)
        return queryset
    '''

class UserProfileViewSet(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend,]
    filter_class = UserFilter

'''
## 기본 view_set 사용한 부분.
post_list = PostViewSet.as_view({
    'get' : 'list',
    'post' : 'create'
})

post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

'''

'''
class PostListView(APIView):
    def get(self,request):
        post_id = request.GET.get('post_id', None)
        if post_id is not None:
            post_data = Post.objects.filter(id=post_id)
        else:
            post_data = Post.objects.all()

        serializer = PostSerializer(post_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

class PostDetailView(APIView):
    def get(self,request,post_id):
        post_data = Post.objects.filter(id=post_id)
        serializer = PostSerializer(post_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,post_id):
        if post_id is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            post_object = Post.objects.get(id=post_id)
            update_post_serializer = PostSerializer(post_object,data=JSONParser().parse(request))
            if update_post_serializer.is_valid():
                update_post_serializer.save()
                return Response(update_post_serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            else:
                return Response(update_post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        try:
            post_object = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            post_object = None

        if post_object is None:
            return Response("No Content Request", status=status.HTTP_404_NOT_FOUND)
        else:
            post_object.delete()
            return Response("Delete Success",status=status.HTTP_204_NO_CONTENT)
'''