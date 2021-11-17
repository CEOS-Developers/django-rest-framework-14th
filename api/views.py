from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import *
from .serializers import *

class PostListView(APIView):
    def get_object(self,pk):
        return get_object_or_404(User,pk=pk)

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
