from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Photo
from .serializers import PhotoSerializer

def photo_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        photo = Photo.objects.all()
        serializer = PhotoSerializer(photo, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PhotoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)