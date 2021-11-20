from django.urls import path
from .views import UserViewSet, PostViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)


urlpatterns = router.urls
'''
urlpatterns = [
    path('users',UserList.as_view()),
    path('posts', PostList.as_view()),
    path('posts/<int:id>', PostDetail.as_view())
]'''