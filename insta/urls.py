from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('profile/', views.profileList.as_view()),
    path('profile/<int:pk>/', views.profileDetail.as_view()),
    # path('profiles/create/', views.profileCreate, name='profile-create'),
    #
    path('post/', views.postListAPIView.as_view()),
    path('post/<int:pk>/', views.postDetailAPIView.as_view()),
    #
    path('follow/', views.followList.as_view()),
    path('follow/<str:pk>/', views.followDetail.as_view()),
]