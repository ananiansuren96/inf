from django.contrib import admin
from .models import Category, Tag, Article, ArticleImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'is_published', 'is_video', 'is_top_news', 'views')
    list_filter = ('category', 'is_published', 'is_video', 'created_at', 'is_top_news')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    inlines = [ArticleImageInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image', 'category', 'tags', 'author', 'content')
        }),
        ('Media', {
            'fields': ('video_url', 'is_video')
        }),
        ('Publication Status', {
            'fields': ('is_published', 'is_top_news', 'views')
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'keywords', 'canonical_url', 'og_image'),
            'classes': ('collapse',)
        }),
    )

