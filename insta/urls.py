from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('profiles/', views.profileList.as_view()),
    path('profiles/<int:pk>/', views.profileDetail.as_view()),
    # path('profiles/create/', views.profileCreate, name='profile-create'),
    #
    path('posts/', views.postList.as_view()),
    path('posts/<int:pk>/', views.postDetail.as_view()),
    #
    path('follows/', views.followList.as_view()),
    path('follows/<str:pk>/', views.followDetail.as_view()),
]