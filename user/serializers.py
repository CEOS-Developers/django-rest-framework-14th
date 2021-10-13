from rest_framework.serializers import ModelSerializer
from user.models import User, Follow


class DynamicFieldsModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        print(kwargs)

        fields = kwargs.pop('fields', None)
        excludes = kwargs.pop('excludes', None)


        print(fields, excludes)

        if fields is not None and excludes is not None:
            raise ValueError

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        elif excludes is not None:
            not_allowed = set(excludes)
            for exclude_name in not_allowed:
                self.fields.pop(exclude_name)


class FollowingSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'to_user']


class FollowerSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'from_user']


class UserSerializer(DynamicFieldsModelSerializer):
    follower = FollowerSerializer(many=True, read_only=True)
    following = FollowingSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'login_id', 'email', 'nickname', 'bio', 'follower', 'following', 'profile_picture']
        exclude = []
