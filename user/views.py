from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from .serializers import UserSerializer
from user.models import User, Follow


@csrf_exempt
@api_view(['GET', 'POST'])
# /api/user
def user_list(request):
    # display all user list
    if request.method == 'GET':
        users = User.objects.all()
        fields = request.GET.getlist('fields') or None
        excludes = request.GET.getlist('excludes') or None

        try:
            serializer = UserSerializer(users, fields=fields, excludes=excludes, many=True)
        except ValueError:
            return JsonResponse({'message': 'Wrong url parameter : '
                                            'Fields and Excludes cannot exist at the same time'}, status=400)

        response = serializer.data
        return JsonResponse(response, status=200, safe=False)

    # create user
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400, safe=False)

        User.objects.create(serializer.data)

        response = serializer.data
        return JsonResponse(response, status=201, safe=False)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
# /api/user/{user_id}
def user_detail(request, pk):
    # display a user
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=pk)

        except User.DoesNotExist:
            return JsonResponse({'message': "Id " + str(pk) + ' doesn\'t exist in database'}, status=404)

        fields = request.GET.getlist('fields') or None

        serializer = UserSerializer(user, fields=fields, many=True)

        response = serializer.data
        return JsonResponse(response, status=200, safe=False)

    # modify a user information
    elif request.method == 'PUT':
        data = JSONParser().parse(request)

        try:
            user = User.objects.get(pk=pk)
            User.objects.update(user, data)

        except User.DoesNotExist:
            return JsonResponse({"message": "Id " + str(pk) + " is not exist"}, status=304)
        except IntegrityError:
            return JsonResponse({"message": str(data) + " is already exist"}, status=304)
        except AttributeError:
            return JsonResponse({"message": str(data) + " have wrong attribute"}, stauts=304)

        return JsonResponse({"message": "Id " + str(pk) + ' is updated successfully'}, status=200)

    # delete a user
    if request.method == 'DELETE':
        try:
            User.objects.delete(pk=pk)

        except ValueError:
            return JsonResponse({'message': 'Id ' + str(pk) + ' doesn\'t exist in database'}, status=304)

        return JsonResponse({'message': 'Id ' + str(pk) + ' is deleted successfully'}, status=200)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
# /api/user/{from_user_id}/following/{to_user_id}
def follow_user(request, from_user_id, to_user_id):
    # check if a user follows target user
    if request.method == 'GET':
        try:
            from_user = User.objects.get(pk=from_user_id)
            to_user = User.objects.get(pk=to_user_id)

        except User.DoesNotExist:
            return JsonResponse({'message': 'id=%s user or id=%s user '
                                            'does not exist in the database' % (from_user_id, to_user_id)}, status=404)

        if from_user.is_following(to_user):
            return JsonResponse({"message": "True"}, status=200)
        return JsonResponse({"message": "False"}, status=200)

    # follow from -> to
    elif request.method == 'PUT':
        try:
            from_user = User.objects.get(pk=from_user_id)
            to_user = User.objects.get(pk=to_user_id)

        except User.DoesNotExist:
            return JsonResponse({'message': 'id=%s user or id=%s user '
                                            'does not exist in the database' % (from_user_id, to_user_id)}, status=404)

        try:
            User.objects.follow(from_user, to_user)

        except ValueError:
            return JsonResponse({"message": str(from_user_id) + ' already followed ' + str(to_user_id)}, status=304)

        return JsonResponse({"message": 'followed ' + str(to_user_id) + ' successfully'}, status=200)

    # a user unfollows target user
    elif request.method == 'DELETE':
        try:
            relation = Follow.objects.get(from_user__id=from_user_id, to_user__id=to_user_id)

        except Follow.DoesNotExist:
            return JsonResponse({"message": str(from_user_id) + ' is not following ' + str(to_user_id)}, status=404)

        relation.delete()
        return JsonResponse({"message": 'unfollowed ' + str(to_user_id) + ' successfully'}, status=200)


@api_view(['GET'])
# /api/user/{user_id}/follower
def follower_list(request, pk):
    # display a user follower list
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=pk)

        except User.DoesNotExist:
            return JsonResponse({'message': '%s does not exist' % (str(pk))}, status=404)

        user_followers = User.objects.filter(following__to_user=user)

        try:
            serializer = UserSerializer(
                user_followers,
                fields=('id', 'login_id', 'email', 'nickname', 'bio', 'profile_picture'),
                many=True
            )

        except ValueError:
            return JsonResponse({'message': 'Wrong url parameter : '
                                            'Fields and Excludes cannot exist at the same time'}, status=404)

        return JsonResponse(serializer.data, safe=False, status=200)


@api_view(['GET'])
# /api/user/{user_id}/following
def following_list(request, pk):
    # display a user following list
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=pk)

        except User.DoesNotExist:
            return JsonResponse({'message': '%s does not exist' % (str(pk))}, status=404)

        user_followings = User.objects.filter(follower__from_user=user)

        try:
            serializer = UserSerializer(
                user_followings,
                fields=('id', 'login_id', 'email', 'nickname', 'bio', 'profile_picture'),
                many=True
            )

        except ValueError:
            return JsonResponse({'message': 'Wrong url parameter : '
                                            'Fields and Excludes cannot exist at the same time'}, status=404)

        return JsonResponse(serializer.data, safe=False, status=200)
