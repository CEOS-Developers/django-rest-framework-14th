from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import UserSerializer, PostSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class UserList(APIView):
    # get all user list, get specific user data
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        queryset = request.GET.get('id', None)
        if queryset is not None:
            try:
                user = User.objects.get(profile__id=queryset)
                serializer = UserSerializer(user, many=False)
                return Response(serializer.data, status=201)
            except ObjectDoesNotExist:
                return Response({"해당하는 유저가 없습니다."}, status=404)
        else:
            user = User.objects.all()
            serializer = UserSerializer(user, many=True)
            return Response(serializer.data, status=201)

    # post new user
    # noinspection PyMethodMayBeStatic
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            u = User.objects.get(username=data['username'])
            p = Profile.objects.create(user=u, photo=data['photo'])
            p.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class PostList(APIView):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        queryset = request.GET.get('id', None)
        if queryset is not None:
            try:
                posts = Post.objects.filter(user__user_id=queryset).all()
                serializer = PostSerializer(posts, many=True)
                return Response(serializer.data, status=201)
            # user id를 잘못 준 경우를 포함한 오류
            except Exception:
                return Response({"해당하는 유저가 없습니다."}, status=404)
        else:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=201)

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        try:
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
            return Response(serializer.data, status=201)
        except ObjectDoesNotExist:
            return Response({"해당하는 유저가 없습니다."}, status=404)


def get_object(post_id):
    try:
        return Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404


class PostDetail(APIView):
    # noinspection PyMethodMayBeStatic
    def put(self, request, post_id):
        # 일단은 post id로 찾긴 하는데 user_id로 검증 한 번 더 필요
        post = get_object(post_id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # noinspection PyMethodMayBeStatic
    def delete(self, request, post_id):
        # 여기도 마찬가지로 사용자 검증 필요
        post = get_object(post_id)
        post.delete()
        return Response({"post id : " + str(post_id) + " 가 성공적으로 삭제되었습니다."}, status=204)

