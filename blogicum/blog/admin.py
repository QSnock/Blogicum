from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.html import format_html

from .models import Post, Category, Location, Comment

User = get_user_model()

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'post_count'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    @admin.display(description='Количество постов')
    def post_count(self, obj):
        return obj.posts.count()


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1
    fields = ('author', 'text')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'comment_count',
        'image_preview',
        'is_published'
    )
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'author__username')
    inlines = [CommentInline]

    @admin.display(description='Комментарии')
    def comment_count(self, obj):
        return obj.comments.count()

    @admin.display(description='Превью')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50">', obj.image.url)
        return 'Нет фото'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'text')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username', 'post__title')
    raw_id_fields = ('post', 'author')
