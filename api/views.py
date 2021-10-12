from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import PostSerializer


# Create your views here.
@csrf_exempt
def post_view(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)  # JSONParser 객체를 생성하고 request에서 데이터 추출
        serializer = PostSerializer(data=data)  # 추출한 데이터를 이용해서 pythonic data 만듬
        if serializer.is_valid():  # 데이터가 유효할 경우
            temp_user = User.objects.get(id=1)  # (임시) 유저 1번이 작성한 게시물인 것처럼
            serializer.save(user=temp_user)  # 요청받은 데이터 저장
            return JsonResponse(serializer.data, status=201, safe=False)  # status 201 created

        # 유효하지 않은 데이터일 경우 error 발생, status 400 bad request
        return JsonResponse(serializer.errors, status=400)
