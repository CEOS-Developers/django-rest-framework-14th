from django.http import JsonResponse
from django.db.utils import IntegrityError

from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from .serializers import FollowerSerializer, FollowingSerializer, UserSerializer
from user.models import User, Follow


class UserView(APIView):
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk=None, **kwargs):
        fields = request.GET.getlist('fields') or None
        if pk is None:
            users = User.objects.all()

            try:
                serializer = UserSerializer(users, fields=fields, many=True)
                return JsonResponse(serializer.data, status=200, safe=False)
            except ValueError:
                return JsonResponse({'message': 'Wrong url parameter'})

        else:
            try:
                user = User.objects.get(pk=pk)
                serializer = UserSerializer(user, fields=fields)
                return JsonResponse(serializer.data, status=200, safe=False)

            except User.DoesNotExist:
                return JsonResponse({'message': "Id " + str(pk) + ' doesn\'t exist in database'}, status=404)

    def post(self, request, pk=None):
        if pk is None:
            data = JSONParser().parse(request)
            fields = ['id', 'nickname', 'login_id', 'email']
            serializer = UserSerializer(data=data, fields=fields)
            if not serializer.is_valid():
                return JsonResponse(serializer.errors, status=400, safe=False)
            serializer.save()
            return JsonResponse(serializer.data, status=201, safe=False)

        else:
            return JsonResponse({'message': 'Wrong url'}, status=400)

    def put(self, request, pk=None):
        try:
            user = self.get_object(pk)
            data = JSONParser().parse(request)
            serializer = UserSerializer(instance=user, data=data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

            return JsonResponse({"message": "Id " + str(pk) + ' is updated successfully'}, status=200)

        except IntegrityError:
            return JsonResponse({"message": str(data) + " is already exist"}, status=304)
        except AttributeError:
            return JsonResponse({"message": str(data) + " have wrong attribute"}, status=304)

    def delete(self, request, pk=None):
        user = self.get_object(pk)
        user.delete()
        return JsonResponse({"message": "Id=%s is deleted successfully" % str(pk)}, status=200)


class FollowView(APIView):
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def is_following(self, from_user_id, to_user_id):
        return Follow.objects.filter(from_user_id=from_user_id, to_user_id=to_user_id).exists()

    def get(self, request, from_user_id, to_user_id):
        if self.is_following(from_user_id, to_user_id):
            return JsonResponse({"message": "True"}, status=200)
        return JsonResponse({"message": "False"}, status=200)

    def put(self, request, from_user_id, to_user_id):
        try:
            if from_user_id == to_user_id:
                return JsonResponse({'message': 'You can\'t follow yourself'}, status=400)

            if self.is_following(from_user_id, to_user_id):
                raise ValueError

            Follow(from_user_id=from_user_id, to_user_id=to_user_id).save()

            return JsonResponse({"message": 'followed ' + str(to_user_id) + ' successfully'}, status=200)

        # FK constraint catch
        except IntegrityError:
            return JsonResponse({"message": 'requested ID doesn\'t exist'}, status=400)

        except ValueError:
            return JsonResponse({"message": str(from_user_id) + ' already followed ' + str(to_user_id)}, status=304)
        

    def delete(self, request, from_user_id, to_user_id):
        if self.is_following(from_user_id, to_user_id):
            Follow.objects.get(from_user_id=from_user_id, to_user_id=to_user_id).delete()
            return JsonResponse({"message": "successfully unfollowed %s" % (str(to_user_id))}, status=200)
        return JsonResponse({"message": "already unfollowed %s" % (str(to_user_id))}, status=200)


class FollowerList(APIView):
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk=None):
        followers = Follow.objects.filter(to_user_id=pk)
        serializer = FollowerSerializer(followers, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
        

class FollowingList(APIView):
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk=None):
        followings = Follow.objects.filter(from_user_id=pk)
        serializer = FollowingSerializer(followings, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
