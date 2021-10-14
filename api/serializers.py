from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'photo']


class UserSerializer(serializers.ModelSerializer):
    # OneToOne Relationship Searialzer (Profile)
    photo = serializers.CharField(source='profile.photo', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'photo', 'username', 'password']
