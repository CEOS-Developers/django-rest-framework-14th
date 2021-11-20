from rest_framework import routers
from .views import UserViewSet, PostViewSet
from django.urls import path

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'post', PostViewSet)

urlpatterns = router.urls
