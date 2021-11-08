from MySQLdb import IntegrityError
from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from .serializers import UserSerializer
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
            serializer = UserSerializer(validated_data=data, fields=fields)
            if not serializer.is_valid():
                return JsonResponse(serializer.errors, status=400, safe=False)
            serializer.save()
            return JsonResponse(serializer.data, status=201, safe=False)

        else:
            return JsonResponse({'message': 'Wrong url'}, status=400)

    def put(self, request, pk=None):
        if pk is None:
            return JsonResponse({"message": "Wrong Url"}, status=400)

        try:
            data = JSONParser().parse(request)
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

            return JsonResponse({"message": "Id " + str(pk) + ' is updated successfully'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message": "Id " + str(pk) + " is not exist"}, status=304)
        except IntegrityError:
            return JsonResponse({"message": str(data) + " is already exist"}, status=304)
        except AttributeError:
            return JsonResponse({"message": str(data) + " have wrong attribute"}, status=304)

    def delete(self, request, pk=None):
        if pk is None:
            return JsonResponse({"message": "Wrong Url"}, status=400)
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return JsonResponse({"message": "Id=%s is deleted successfully" % str(pk)}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message": "Id " + str(pk) + " is not exist"}, status=304)


class FollowView(APIView):
    def get(self, request, from_user_id, to_user_id):
        try:
            from_user = User.objects.get(pk=from_user_id)
            to_user = User.objects.get(pk=to_user_id)
            if from_user.is_following(to_user):
                return JsonResponse({"message": "True"}, status=200)
            return JsonResponse({"message": "False"}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'message': 'id=%s user or id=%s user '
                                            'does not exist in the database' % (from_user_id, to_user_id)}, status=400)

    def put(self, request, from_user_id, to_user_id):
        try:
            if from_user_id == to_user_id:
                return JsonResponse({'message': 'You can\'t follow yourself'}, status=400)

            follow = Follow.objects.filter(from_user_id=from_user_id) & Follow.objects.filter(to_user_id=to_user_id)

            if follow.count() > 0:
                raise ValueError

            Follow(from_user_id=from_user_id, to_user_id=to_user_id).save()

            return JsonResponse({"message": 'followed ' + str(to_user_id) + ' successfully'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'message': 'id=%s user or id=%s user '
                                            'does not exist in the database' % (from_user_id, to_user_id)}, status=404)
        except ValueError:
            return JsonResponse({"message": str(from_user_id) + ' already followed ' + str(to_user_id)}, status=304)

    def delete(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return JsonResponse({"message": "Id=%s is deleted successfully" % str(pk)}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message": "Id " + str(pk) + " is not exist"}, status=304)


class FollowerList(APIView):
    def get(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            followers = User.objects.filter(following__to_user=user)
            serializer = UserSerializer(followers, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)

        except User.DoesNotExist:
            return JsonResponse({'message': '%s does not exist' % (str(pk))}, status=400)
        except ValueError:
            return JsonResponse({'message': 'Wrong url parameter : '
                                            'Fields and Excludes cannot exist at the same time'}, status=404)


class FollowingList(APIView):
    def get(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            followings = User.objects.filter(follower__from_user=user)
            serializer = UserSerializer(followings, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)

        except User.DoesNotExist:
            return JsonResponse({'message': '%s does not exist' % (str(pk))}, status=400)
        except ValueError:
            return JsonResponse({'message': 'Wrong url parameter : '
                                            'Fields and Excludes cannot exist at the same time'}, status=404)
