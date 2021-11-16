from django.contrib.admin.utils import lookup_field
from django_filters.rest_framework import FilterSet, filters
from rest_framework.generics import get_object_or_404
from .models import *


class PostFilter(FilterSet):
    following = filters.NumberFilter(method='filter_following_posts', label='user_id')

    class Meta:
        model = Post
        fields = {
            'created_date': ['lt', 'gt']
        }

    # user가 팔로우하는 계정의 post만 가져오도록.
    def filter_following_posts(self, queryset, name, value):
        user = get_object_or_404(User, pk=value)
        filtered_posts = queryset.filter(author__followers__follower=user)
        return filtered_posts


class UserFilter(FilterSet):
    nickname = filters.CharFilter(field_name='nickname', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['nickname']













