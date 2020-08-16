from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from .models import Base, Post, Category, Tag, SiteDetail, AboutSite, PrivacyPolicy, Snippet, Image, Link, PopularPost

""" すべてのページで呼ぶコンテキスト """
def common(request):
    context = {
        'popular_posts': PopularPost.objects.order_by('-page_view')[:5],
        'recent_posts': Post.objects.select_related('category').filter(is_public=True).order_by('-published_at', '-created_at')[:5],
        'categories': Category.objects.annotate(count=Count('post', filter=Q(post__is_public=True))).exclude(count=0).order_by('-count', 'name')[:10],
        'tags': Tag.objects.select_related('category').annotate(count=Count('post', filter=Q(post__is_public=True))).exclude(count=0).order_by('-count', 'name')[:10],
        'archives': Post.objects.select_related('category').prefetch_related('tag').filter(is_public=True).annotate(month=TruncMonth('published_at')).values('month').order_by('-month').distinct().annotate(count=Count('pk'))[:10],
    }
    return context

""" デバッグ判定 """
def is_debug(request):
    return {"DEBUG": settings.DEBUG}