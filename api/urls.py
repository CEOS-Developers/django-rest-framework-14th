from django.urls import path
from api import views

urlpatterns = [
    path('profile/<int:profile_id>/', views.profile_detail),
    path('posts/', views.post_list),
    path('post/<int:post_id>/', views.post_detail),
    path('comments/', views.comment_create),
    path('comment/<int:comment_id>/', views.comment_detail),
    path('likes/', views.like_create)
]
