from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.profile_list)
]