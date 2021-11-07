from django.urls import path
from .views import user_list, post_list

urlpatterns = [
    path('users',user_list),
    path('posts', post_list),
]