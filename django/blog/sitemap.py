from django.contrib.sitemaps import Sitemap
from django.urls import reverse_lazy
from django.shortcuts import resolve_url
from .models import Post, Category, Tag

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return Post.objects.select_related('category').prefetch_related('tag').filter(is_public=True).order_by('-published_at')

    def lastmod(self, obj):
        return obj.published_at

    def location(self, obj):
        return reverse_lazy('blog:detail', kwargs={'pk': obj.pk})

class IndexSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ['blog:index', 'blog:category', 'blog:tag', 'blog:archive']

    def location(self, obj):
        return reverse_lazy(obj)

class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Category.objects.order_by('index')

    def location(self, obj):
        return reverse_lazy('blog:category_post', kwargs={'category': obj.slug})

class TagSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Tag.objects.all().order_by('slug').select_related('category')

    def location(self, obj):
        return reverse_lazy('blog:tag_post', kwargs={'tag': obj.slug})

class PostArchiveYearSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Post.objects.select_related('category').prefetch_related('tag').filter(is_public=True) \
            .values('published_at__year') \
            .order_by('-published_at__year').distinct()

    def location(self, obj):
        year = list(obj.values())[0]
        return resolve_url('blog:archive_year', year=year)

class PostArchiveMonthSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Post.objects.select_related('category').prefetch_related('tag').filter(is_public=True) \
            .values('published_at__year','published_at__month') \
            .order_by('-published_at__year','-published_at__month').distinct()

    def location(self, obj):
        year = list(obj.values())[0]
        month = format(list(obj.values())[1], '0>2')
        return resolve_url('blog:archive_month', year=year, month=month)

class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['blog:about', 'blog:policy', 'blog:report']

    def location(self, obj):
        return reverse_lazy(obj)