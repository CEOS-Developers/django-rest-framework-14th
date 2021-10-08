from django.contrib import admin
from .models import Profile, Post, Photo, Video, Like, Comment, FollowRelation


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Video)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(FollowRelation)
