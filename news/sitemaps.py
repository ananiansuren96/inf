from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article, Category

class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Article.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
        
    def location(self, obj):
        return reverse('article_detail', args=[obj.slug])

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('category_detail', args=[obj.slug])
