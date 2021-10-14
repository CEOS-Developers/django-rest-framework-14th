from django.urls import path
from .views import LikeViewSet, ProfileViewSet, PostViewSet, CommentViewSet


profile_detail = ProfileViewSet.as_view({ 'get': 'retrieve' })

post_list = PostViewSet.as_view({
    'post': 'create',
    'get': 'list'
})

post_detail = PostViewSet.as_view({ 'get': 'retrieve' })

comment = CommentViewSet.as_view({ 'post': 'create' })

comment_detail = CommentViewSet.as_view({
    'post': 'create',
    'get': 'retrieve'
})

like = LikeViewSet.as_view({ 'post': 'create' })

urlpatterns = [
    path('profile/<int:pk>/', profile_detail),
    path('posts/', post_list),
    path('post/<int:pk>/', post_detail),
    path('comments/', comment),
    path('comment/<int:pk>/', comment_detail),
    path('likes/', like)
]
