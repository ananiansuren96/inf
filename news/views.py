from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from .models import Article, Category

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Top News (Main banner)
        top_news = Article.objects.filter(is_published=True, is_top_news=True).first()
        context['top_news'] = top_news
        
        # Side News (Next to main banner)
        if top_news:
            side_news = Article.objects.filter(is_published=True).exclude(id=top_news.id)[:4]
        else:
            side_news = Article.objects.filter(is_published=True)[:4]
        context['side_news'] = side_news

        # Categories with their latest news
        categories = Category.objects.all()
        category_news = {}
        for cat in categories:
            news = cat.articles.filter(is_published=True)[:4]
            if news:
                category_news[cat] = news
        context['category_news'] = category_news

        # Video News
        video_news = Article.objects.filter(is_published=True, is_video=True)[:3]
        context['video_news'] = video_news

        # Trending (Most viewed in last 24h - simplified to just most viewed for now)
        context['trending'] = Article.objects.filter(is_published=True).order_by('-views')[:5]
        
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related news (same category)
        context['related_news'] = Article.objects.filter(
            category=self.object.category, 
            is_published=True
        ).exclude(id=self.object.id)[:3]
        return context

class CategoryListView(ListView):
    model = Article
    template_name = 'category_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        queryset = Article.objects.filter(category=self.category, is_published=True)
        
        sort = self.request.GET.get('sort')
        if sort == 'popular':
            queryset = queryset.order_by('-views')
        else: # newest is default
            queryset = queryset.order_by('-created_at')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class SearchView(ListView):
    model = Article
    template_name = 'search_results.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Article.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(tags__name__icontains=query),
                is_published=True
            ).distinct()
        return Article.objects.none()
