from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

# 추가
from rest_framework import routers
from .views import PostViewSet, UserViewSet, FollowViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)
router.register(r'follows', FollowViewSet)

urlpatterns = router.urls

# urlpatterns = [
#
#     path('users', views.userList.as_view()),
#     path('users/<int:pk>', views.userDetail.as_view()),
#     #
#     path('posts', views.postList.as_view()),
#     path('posts/<int:pk>', views.postDetail.as_view()),
#     #
#     path('follow', views.followList.as_view()),
#     path('following/<int:pk>', views.following.as_view()),
#     path('followee/<int:pk>', views.followee.as_view()),
# ]