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
        # 추출한 데이터를 이용해서 pythonic data 만듬
        serializer = PostSerializer(data=data)
        if serializer.is_valid():  # 데이터가 유효할 경우
            # (임시) user1이 작성한 게시물인 것으로 저장
            # 추후에는 현재 로그인한 유저정보를 request.user로 받아와서 저장하면 됨
            temp_user = User.objects.get(id=1)
            serializer.save(user=temp_user)  # 요청받은 데이터 저장
            # status 201 created
            return JsonResponse(serializer.data, status=201, safe=False)

        # 유효하지 않은 데이터일 경우 error 발생, status 400 bad request
        return JsonResponse(serializer.errors, status=400)
