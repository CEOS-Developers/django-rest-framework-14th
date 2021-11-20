from django.urls import path

from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from api.views import LoginView, LogoutView

from user.views import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename="user")

urlpatterns = router.urls
urlpatterns += [
  path('login', LoginView.as_view()),
  path('logout', LogoutView.as_view()),
  path('token', obtain_jwt_token),
  path('token/verify', verify_jwt_token),
  path('token/refresh', refresh_jwt_token),
]