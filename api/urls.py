from django.urls import path, include
from rest_framework import routers
from .views import PostList, PostDetail

# router = routers.DefaultRouter()
# router.register(r'posts', PostViewSet)

urlpatterns = [
    # path('', include(router.urls))
    path('posts/', PostList.as_view()),
    path('posts/<int:pk>/', PostDetail.as_view())
]
