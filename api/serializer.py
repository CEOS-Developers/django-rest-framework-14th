from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend

from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework_jwt.settings import api_settings

from user.models import User

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class LoginBackend(ModelBackend):
    def authenticate(self, request, login_id=None, password=None, **kwargs):
        try:
            user = User.objects.get(login_id=login_id)
            if user.check_password(password):
                return user
            return None

        except User.DoesNotExist:
            return None

class LoginSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False, read_only=True)
    login_id = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=30, write_only=True)
    token = serializers.CharField(max_length=300, read_only=True)

    def validate(self, data):
        login_id = data.get('login_id', None)
        password = data.get('password', None)
        user = authenticate(login_id=login_id, password=password)
        if user is None:
            raise serializers.ValidationError(detail=True)

        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        
        return {
            'id':user.id,
            'login_id':login_id,
            'token':jwt_token
        }