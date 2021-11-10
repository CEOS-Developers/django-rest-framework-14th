from django.contrib import admin
from django.db.models import Count

from .models import *

# Register your models here.


class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    """
    이 코드는  N+1 problem을 야기하기 때문에 다른 방식을 사용하는 것이 좋다.
    def post_comment_count(self,obj):
        return obj.comment_set.count()
    """
    def comment_count(self,obj):
        return obj.comment_count

    def like_count(self,obj):
        return obj.like_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(comment_count = Count("post_comments"), like_count = Count("post_likes"))
        return queryset

    comment_count.short_description = "Comments count"
    comment_count.admin_order_field = 'comment_count'   # make the column sortable.
    like_count.admin_order_field = 'like_count'
    inlines = [CommentInline]
    list_display = ['id', 'title', 'author', 'comment_count', 'like_count','created_date', 'updated_date']
    list_display_links = ['id','title']
    list_per_page = 10

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Like)
