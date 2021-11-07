from django.urls import path
from .views import post_view

urlpatterns = [
    path('posts', post_view)
]
