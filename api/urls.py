from django.urls import path
from .views import UserList, PostList, PostDetail

urlpatterns = [
    path('users',UserList.as_view()),
    path('posts', PostList.as_view()),
    path('posts/<int:id>', PostDetail.as_view())
]