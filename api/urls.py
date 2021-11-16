from django.urls import path
from .views import PostDetail, PostList

urlpatterns = [
    path('posts', PostList.as_view()),
    path('posts/<int:pk>', PostDetail.as_view()),
]
