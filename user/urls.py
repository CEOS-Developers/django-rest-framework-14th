from django.urls import include, path
from user import views


urlpatterns = [
    path('', views.user_list),
    path('/<int:pk>', views.user_detail),
    path('/<int:pk>/follower', views.follower_list),
    path('/<int:pk>/following', views.following_list),
    path('/<int:from_user_id>/following/<int:to_user_id>', views.follow_user)
]