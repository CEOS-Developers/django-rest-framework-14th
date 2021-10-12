from rest_framework import serializers
from user.models import User, Follow


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'to_user']


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'from_user']


class UserSerializer(serializers.ModelSerializer):
    follower = FollowerSerializer(many=True, read_only=True)
    following = FollowingSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'bio', 'profile_picture', 'is_private', 'is_active', 'following',
                  'follower']
