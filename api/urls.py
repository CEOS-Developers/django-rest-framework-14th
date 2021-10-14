from django.urls import path
from .views import PostViewSet

post_list = PostViewSet.as_view({
  'post': 'create',
  'get': 'list'
})

urlpatterns = [
    path('posts/', post_list),
]
