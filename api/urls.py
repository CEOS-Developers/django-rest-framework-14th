
from rest_framework import routers
from api.views import PostViewSet, ProfileViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = router.urls
