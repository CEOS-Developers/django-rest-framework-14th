from django.urls import include, path

urlpatterns = [
    path('user', include('user.urls')),
    # path('post', include('post.urls')),
    # path('comment', include('comment.urls')),
    # path('hashtag', include('hashtag.urls')),
]