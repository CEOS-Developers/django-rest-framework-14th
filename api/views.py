from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from .models import *
from .serializers import UserSerializer, PostSerializer


@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            u = User.objects.get(username=data['username'])
            p = Profile.objects.create(user=u, photo=data['photo'])
            p.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        queryset = request.GET.get('q', None)
        if queryset is not None:
            posts = Post.objects.filter(user__user_id=queryset).all()
            serializer = PostSerializer(posts, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        profile_id = request.data.get('profile_id')
        images_data = request.data.get('images')
        text = request.data.get('text')
        post = Post.objects.create(
            user=Profile.objects.get(user_id=profile_id),
            text=text
        )
        for image_data in images_data:
            Image.objects.create(post=post, image=image_data)
        serializer = PostSerializer(post, many=False)
        return JsonResponse(serializer.data, status=201)
