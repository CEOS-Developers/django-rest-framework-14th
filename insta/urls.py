from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('users', views.userList.as_view()),
    path('users/<int:pk>', views.userDetail.as_view()),
    #
    path('posts', views.postList.as_view()),
    path('posts/<int:pk>', views.postDetail.as_view()),
    #
    path('follow', views.followList.as_view()),
    path('following/<int:pk>', views.following.as_view()),
    path('followee/<int:pk>', views.followee.as_view()),
]