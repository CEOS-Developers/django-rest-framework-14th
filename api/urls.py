from django.urls import path
from . import views

urlpatterns = [
    path('photo/', views.photo_list)
]