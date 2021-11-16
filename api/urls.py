
from rest_framework import routers
from api.views import PostViewSet, ProfileViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basname='post')
router.register(r'users', ProfileViewSet, basename='users')

urlpatterns = router.urls
