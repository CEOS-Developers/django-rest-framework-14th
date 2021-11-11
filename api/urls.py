from django.urls import path
from api import views

urlpatterns = [
    path('posts/', views.post_list),
    path('posts/<int:pk>', views.post_detail)
]
