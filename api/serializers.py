from api.models import Profile
from rest_framework import serializers

class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    website = serializers.CharField(required=False, allow_blank=True, max_length=40)
    introduction = serializers.CharField(allow_blank=True)
    phone_num = serializers.IntegerField(allow_null=False)
    gender = serializers.CharField()

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    def update(self,instance,validated_data):
        instance.website =validated_data.get('website',instance.website)
        instance.introduction = validated_data.get('introduction',instance.introduction)
        instance.phone_num = validated_data.get('phone_num', instance.phone_num)
        instance.gender = validated_data.get('gender',instance.gender)
        instance.save()
        return instance
