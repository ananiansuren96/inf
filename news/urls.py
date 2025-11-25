from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category_detail'),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
]
