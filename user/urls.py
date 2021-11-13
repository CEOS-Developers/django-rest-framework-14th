from django.urls import include, path
from user.views import *

urlpatterns = [
    path('', UserView.as_view()),
    path('/<int:pk>', UserView.as_view()),
    path('/<int:from_user_id>/following/<int:to_user_id>', FollowView.as_view()),
    path('/<int:pk>/follower', FollowerList.as_view()),
    path('/<int:pk>/following', FollowingList.as_view())
]