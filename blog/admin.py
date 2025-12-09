# blog/admin.py
from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Category, Lesson, Resource


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'slug', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Lesson)
class LessonAdmin(MarkdownxModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'status', 'published_at', 'views_count']
    list_filter = ['category', 'difficulty', 'status', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'

    fieldsets = (
        ('Podstawowe', {
            'fields': ('title', 'slug', 'category')
        }),
        ('Treść', {
            'fields': ('excerpt', 'content')
        }),
        ('Metadane', {
            'fields': ('difficulty', 'status', 'published_at')
        }),
        ('Statystyki', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/markdownx_fix.css',)
        }


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'url', 'order', 'created_at']
    list_filter = ['resource_type', 'is_external', 'created_at']
    search_fields = ['title', 'description', 'url']
    list_editable = ['order']
    ordering = ['order', '-created_at']

    fieldsets = (
        ('Podstawowe', {
            'fields': ('title', 'description', 'url')
        }),
        ('Kategoryzacja', {
            'fields': ('resource_type', 'is_external')
        }),
        ('Ustawienia', {
            'fields': ('order',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()