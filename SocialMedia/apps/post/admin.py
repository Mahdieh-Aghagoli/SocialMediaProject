from django.contrib import admin
from apps.post.models.post import Post, Comment, Preference


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['content', 'date_posted', 'author', ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'date_posted', 'author', 'post_connected']


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'value', 'date']
