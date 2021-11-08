from rest_framework.serializers import ModelSerializer, SerializerMethodField
from user.models import User, Follow


class DynamicFieldsModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class FollowingSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'to_user']


class FollowerSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'from_user']


class UserSerializer(DynamicFieldsModelSerializer):
    follower_nickname = SerializerMethodField()
    following_nickname = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'login_id', 'email',
            'nickname', 'bio', 'profile_picture',
            'follower_nickname',
            'following_nickname',
            'is_private', 'is_active', 'is_superuser',
            'created_date'
        ]

    def create(self, validated_data):
        user = User(
            nickname=validated_data.get('nickname'),
            email=validated_data.get('email'),
            login_id=validated_data.get('login_id')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.is_private = validated_data.get('is_private', instance.is_private)
        instance.save()
        return instance

    def get_follower_nickname(self, obj):
        followers = obj.follower.select_related('from_user').all()
        ret = [follower.from_user.nickname for follower in followers]
        return ret

    def get_following_nickname(self, obj):
        followings = obj.following.select_related('to_user').all()
        ret = [following.to_user.nickname for following in followings]
        return ret
