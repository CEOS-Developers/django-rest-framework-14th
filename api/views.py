from .models import *
from .serializers import UserSerializer, PostSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # 특정 유저의 모든 post 조회
    def list(self, request, *args, **kwargs):
        query_params = request.query_params
        self.queryset = self.get_queryset().filter(user__id__icontains=query_params.get('user_id')).order_by('-updated_at')
        return super().list(request, *args, **kwargs)


'''
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
        print("data type : ")
        print(type(request.data))
        print("post type : ")
        print(type(post))
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
'''
