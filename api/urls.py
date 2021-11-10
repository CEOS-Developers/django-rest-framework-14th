from django.urls import path
from .views import *

urlpatterns = [
    path('posts/', PostListView.as_view(),name='post-list'),
    path('posts/<int:post_id>', PostDetailView.as_view())
]