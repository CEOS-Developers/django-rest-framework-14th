from django.contrib import admin
from user.models import User
from post.models import Post 
from comment.models import Comment
from hashtag.models import Hashtag 

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Hashtag)
