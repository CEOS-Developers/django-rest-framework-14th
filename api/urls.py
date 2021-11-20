from rest_framework import routers
from .views import PostViewSet, ProfileViewSet, CommentViewSet, LikeViewSet

router = routers.DefaultRouter()
router.register(r'post', PostViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'like', LikeViewSet)

urlpatterns = router.urls
