from django.urls import include, path
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter, Route, SimpleRouter

from user.views import *
from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'', views.UserViewSet, basename="user")

urlpatterns = router.urls

# urlpatterns = [
#     path('',include(router.urls)),
# ]

# urlpatterns = [
#     path('', UserView.as_view()),
#     path('/<int:pk>', UserView.as_view()),
#     path('/<int:from_user_id>/following/<int:to_user_id>', FollowView.as_view()),
#     path('/<int:pk>/follower', FollowerList.as_view()),
#     path('/<int:pk>/following', FollowingList.as_view())
# ]