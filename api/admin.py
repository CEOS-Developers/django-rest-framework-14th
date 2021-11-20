from django.contrib import admin
from django.contrib import admin
from .models import User, Post

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    display = [field.name for field in User._meta.fields]


class PostAdmin(admin.ModelAdmin):
    display = [field.name for field in Post._meta.fields]


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)