from django.contrib import admin
from .models import Profile, Post, File, Like, Bookmark, Comment, Follow, FollowRelation

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'followee']


# File 클래스를 inline으로 나타내기
class FileInline(admin.TabularInline):
    model = File


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'content']
    inlines = [FileInline, ]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['post', 'user']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'post']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower']


@admin.register(FollowRelation)
class FollowRelationAdmin(admin.ModelAdmin):
    list_display = ['user', 'following']