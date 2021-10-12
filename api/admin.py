from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_text',
                    'get_likes_count',
                    'get_comments_count',
                    'created_at', 'updated_at']
    list_display_links = ['id', 'get_text']

    def get_text(self, post):
        return f'{post.text[:20]} ...'
    get_text.short_description = '내용'

    def get_likes_count(self, post):
        return f'{post.post_likes.count()}개'
    get_likes_count.short_description = '좋아요'

    def get_comments_count(self, post):
        return f'{post.post_comments.count()}개'
    get_comments_count.short_description = '댓글'


admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Like)
admin.site.register(Comment)
