from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = []  # больше нет поля likes, ничего тут не нужно
    list_display = ['id','created_by', 'description', 'like_count']

    def like_count(self, obj):
        return obj.like_set.count()
    like_count.short_description = "Лайков"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'post', 'created_time')
    search_fields = ('created_by__username', 'text')
    list_filter = ('created_time',)
    readonly_fields = ('created_time',)
