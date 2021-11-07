from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import PostSerializer


@csrf_exempt
def post_view(request):

    if request.method == 'GET':
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            temp_user = User.objects.get(id=1)
            serializer.save(post_author=temp_user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
