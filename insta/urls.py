from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.profileList, name='profile-list'),
    path('profiles/<int:pk>/', views.profileDetail, name='profile-detail'),
    path('profiles/create/', views.profileCreate, name='profile-create'),

    path('posts/', views.postList, name='post-list'),
    path('posts/<int:pk>/', views.postDetail, name='post-detail'),

    path('follows/', views.followList, name='follow-list'),
    path('follows/<str:pk>/', views.followDetail, name='follow-detail'),
]