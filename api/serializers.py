from .models import Photo
from rest_framework import serializers

class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    photo_url = serializers.ImageField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        return Photo.objects.create(**validated_data)

    def update(self,instance,validated_data):
        instance.photo_url = validated_data.get('photo_url',instance.photo_url)
        instance.date = validated_data.get('date',instance.date)
        instance.save()
        return instance

    class Meta:
        model = Photo
        fields = {'photo_url', 'date'}
