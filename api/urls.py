from django.urls import path
from api import views

urlpatterns = [
    path('profile/<int:pk>/', views.ProfileDetail.as_view()),
    path('posts/', views.PostList.as_view()),
    path('post/<int:pk>/', views.PostDetail.as_view()),
    path('comments/', views.CommentDetail.as_view()),
    path('comment/<int:pk>/', views.CommentDetail.as_view()),
    path('likes/', views.LikeDetail.as_view())
]
