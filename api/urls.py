from django.urls import path
from api import views
from .views import PostViewSet, UserViewSet
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls

# urlpatterns = [
#     path('posts/', views.PostList.as_view(), name='posts'),
#     path('posts/<int:pk>', views.PostDetail.as_view(), name='post_detail'),
#     path('users/', views.UserList.as_view(), name='users'),
#     path('users/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)