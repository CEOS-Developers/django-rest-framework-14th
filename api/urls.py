from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path(r'posts', PostViewSet.as_view()),
    path(r'user', UserProfileViewSet.as_view())
]
