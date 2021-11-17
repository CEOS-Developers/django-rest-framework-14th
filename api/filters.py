from django.contrib.admin.utils import lookup_field
from django_filters.rest_framework import FilterSet, filters
from rest_framework.generics import get_object_or_404
from .models import *
import re


class PostFilter(FilterSet):
    following = filters.NumberFilter(method='filter_following_posts', label='user_id')

    class Meta:
        model = Post
        fields = {
            'created_date': ['lt', 'gt']
        }

    # user가 팔로우하는 계정의 post만 가져오도록 filtering.
    def filter_following_posts(self, queryset, name, value):
        user = get_object_or_404(User, pk=value)
        filtered_posts = queryset.filter(author__followers__follower=user)
        return filtered_posts


class UserFilter(FilterSet):
    # info에 email 정보를 써둔 계정만 filtering.
    info = filters.BooleanFilter(method='filter_has_email', label='has_email')

    class Meta:
        model = User
        fields = ['profile']

    def filter_has_email(self, queryset, name, value):
        pattern = r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"
        user_with_email = []
        user_without_email = []
        for user in queryset:
            match = re.search(pattern, user.profile.info)
            if match:
                user_with_email.append(user.profile)
            else:
                user_without_email.append(user.profile)

        return queryset.filter(profile__in=user_with_email)
















