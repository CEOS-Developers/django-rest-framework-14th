from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import *
from .serializers import *

class PostListView(APIView):
    def get(self,request):
        post_id = request.GET.get('post_id', None)
        if post_id is not None:
            post_data = Post.objects.filter(id=post_id)
        else:
            post_data = Post.objects.all()

        serializer = PostSerializer(post_data, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self,request):
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class PostDetailView(APIView):
    def get(self,request,post_id):
        post_data = Post.objects.filter(id=post_id)
        serializer = PostSerializer(post_data, many=True)
        return JsonResponse(serializer.data, safe=False)

