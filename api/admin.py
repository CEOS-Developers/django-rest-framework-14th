from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_content',
                    'get_likes_count',
                    'get_comments_count',
                    'location']
    list_display_links = ['id', 'get_content']

    def get_content(self, post):
        return f'{post.post_content[:20]} ...'
    get_content.short_description = '내용'

    def get_likes_count(self, post):
        return f'{post.post_likes.count()}개'
    get_likes_count.short_description = '좋아요'

    def get_comments_count(self, post):
        return f'{post.comment_post.count()}개'
    get_comments_count.short_description = '댓글'


admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Comment)
