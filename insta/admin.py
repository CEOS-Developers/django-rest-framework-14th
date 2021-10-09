from django.contrib import admin
from .models import Profile, Post, Like, Bookmark, Comment

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'photo', 'content']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['post', 'user']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content']


