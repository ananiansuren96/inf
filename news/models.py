from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='articles/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = CKEditor5Field('Content', config_name='extends')
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_top_news = models.BooleanField(default=False)

    # SEO Fields
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(blank=True)
    keywords = models.CharField(max_length=200, blank=True)
    canonical_url = models.URLField(blank=True, help_text="Canonical URL if this content is duplicated")
    og_image = models.ImageField(upload_to='articles/og/', blank=True, help_text="Image for Social Media (OpenGraph)")

    # Video
    video_url = models.URLField(blank=True, help_text="YouTube or Vimeo URL")
    is_video = models.BooleanField(default=False, verbose_name="Video Post", help_text="Check this if the article is primarily a video.")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='articles/gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.article.title}"

