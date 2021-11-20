from django.urls import path
from . import views
from rest_framework import routers
from .views import PostViewSet

# urlpatterns = [
#     path('posts', views.PostList.as_view()),
#     path('posts/<int:pk>', views.PostDetail.as_view())
# ]

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)   # register()함으로써 두 개의 url 생성

urlpatterns = router.urls