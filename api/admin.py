from django.contrib import admin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Like)
admin.site.register(Comment)


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'user_id', 'get_text', 'get_likes_count', 'get_comments_count', 'created_at', 'updated_at']
    list_display_links = ('get_text', 'user')
    list_filter = (
        'user', ('created_at', DateRangeFilter), ('updated_at', DateTimeRangeFilter),
    )

    def get_text(self, post):
        res = post.text
        if len(post.text) > 10:
            res = post.text[0:10] + '...'
        return f'{res}'

    get_text.short_description = '본문'

    def get_likes_count(self, post):
        return f'{post.post_likes.count()}개'

    get_likes_count.short_description = '좋아요'

    def get_comments_count(self, post):
        return f'{post.post_comments.count()}개'

    get_comments_count.short_description = '댓글'


admin.site.register(Post, PostAdmin)
