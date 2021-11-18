from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)

'''
urlpatterns = [
    path('posts', views.post_list),
    path('posts/<int:pk>', views.post_detail),
]
'''

urlpatterns = [
    path('', include(router.urls))
]