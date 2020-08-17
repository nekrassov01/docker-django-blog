from django.urls import path
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView, RedirectView
from . import views
from . import statistics
from .feeds import PostFeed
from .sitemap import PostSitemap, IndexSitemap, CategorySitemap, TagSitemap, PostArchiveYearSitemap, PostArchiveMonthSitemap, StaticSitemap

app_name = 'blog'

sitemaps = {
    'post': PostSitemap,
    'index': IndexSitemap,
    'category': CategorySitemap,
    'tag': TagSitemap,
    'postarchiveyear': PostArchiveYearSitemap,
    'postarchivemonth': PostArchiveMonthSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('tag/', views.TagListView.as_view(), name='tag'),
    path('archive/', views.PostArchiveView.as_view(), name='archive'),
    path('category/<slug:category>/', views.PostCategoryView.as_view(), name='category_post'),
    path('tag/<slug:tag>/', views.PostTagView.as_view(), name='tag_post'),
    path('archive/<slug:year>/', views.PostArchiveYearView.as_view(), name='archive_year'),
    path('archive/<slug:year>/<slug:month>/', views.PostArchiveMonthView.as_view(), name='archive_month'),
    path('detail/<slug:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('draft/', views.PostDraftView.as_view(), name='draft'),
    path('about-site/', views.AboutSiteView.as_view(), name='about'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='policy'),
    path('snippet/', views.SnippetView.as_view(), name='snippet'),
    path('graph/', statistics.statistics, name='graph'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('feed/', PostFeed(), name='feed'),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('ping/', views.ping, name='ping'),
    path('robots.txt/', (TemplateView.as_view(template_name='blog/robots.txt', content_type='text/plain')), name='robots.txt'),
    path('favicon.ico', RedirectView.as_view(url='/static/blog/favicon/favicon.ico')),
    path('favicon.png', RedirectView.as_view(url='/static/blog/favicon/favicon.png')),
]
