from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.contrib.sitemaps import ping_google
from django.views import generic
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.urls import reverse_lazy
from django.http import Http404
from .models import Post, Category, Tag, SiteDetail, AboutSite, PrivacyPolicy, Snippet, Image, Link, PopularPost
from .forms import ContactForm


""" リストビューの基底クラス """
class BaseListView(generic.ListView):
    paginate_by = 10
    label = None

    def get_queryset(self):
        queryset = Post.objects.select_related('category').prefetch_related('tag').filter(is_public=True).order_by('-published_at', '-created_at')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = self.label
        return context

""" 記事一覧 """
class PostListView(BaseListView):
    template_name = 'blog/blog_posts.html'
    model = Post
    label = '記事一覧'

    def get_queryset(self):
        query = self.query = self.request.GET.get('query')
        queryset = super().get_queryset()
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(text__icontains=query) | Q(description__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        return context

""" 下書き一覧"""
class PostDraftView(LoginRequiredMixin, BaseListView):
    template_name = 'blog/blog_posts.html'
    model = Post
    label = '下書き一覧'

    def get_queryset(self):
        query = self.query = self.request.GET.get('query')
        queryset = Post.objects.select_related('category').prefetch_related('tag').filter(is_public=False).order_by('-published_at', '-created_at')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(text__icontains=query) | Q(description__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        return context

""" 記事一覧 | カテゴリーでフィルタ """
class PostCategoryView(BaseListView):
    template_name = 'blog/blog_posts.html'
    model = Post

    def get_queryset(self):
        category = self.category = get_object_or_404(Category, slug=self.kwargs['category'])
        queryset = super().get_queryset().filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['label'] = '[ {} ] カテゴリーの記事一覧'.format(self.category.name)
        return context

""" 記事一覧 | タグでフィルタ """
class PostTagView(BaseListView):
    template_name = 'blog/blog_posts.html'
    model = Post

    def get_queryset(self):
        tag = self.tag = get_object_or_404(Tag, slug=self.kwargs['tag'])
        queryset = super().get_queryset().filter(tag=self.tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['label'] = '[ {} ] タグの記事一覧'.format(self.tag.name)
        return context

""" 記事一覧 | 年でフィルタ """
class PostArchiveYearView(generic.YearArchiveView, BaseListView):
    template_name = 'blog/blog_posts.html'
    model = Post
    date_field = 'published_at'
    allow_empty = True
    make_object_list = True

    def get_queryset(self):
        year = self.year = self.kwargs['year']
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.year
        context['label'] = '{} 年の記事一覧'.format(self.year)
        return context

""" 記事一覧 | 年月でフィルタ """
class PostArchiveMonthView(generic.MonthArchiveView, BaseListView):
    template_name = 'blog/blog_posts.html'
    model = Post
    date_field = 'published_at'
    allow_empty = True
    make_object_list = True
    month_format = '%m'

    def get_queryset(self):
        year = self.year = self.kwargs['year']
        month = self.month = self.kwargs['month']
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.year
        context['month'] = self.month
        context['label'] = '{} 年 {} 月の記事一覧'.format(self.year, self.month)
        return context

""" アーカイブ一覧 """
class PostArchiveView(generic.ArchiveIndexView, BaseListView):
    template_name = 'blog/blog_table_archive.html'
    model = Post
    date_field = 'published_at'
    allow_empty = True
    paginate_by = None
    label = 'アーカイブ'

    def get_queryset(self):
        queryset = super().get_queryset().annotate(month=TruncMonth('published_at')).values('month').order_by('month').distinct().annotate(count=Count('pk'))
        return queryset

""" カテゴリ一覧 """
class CategoryListView(BaseListView):
    template_name = 'blog/blog_table_category.html'
    model = Category
    ordering = 'index'
    paginate_by = None
    label = 'カテゴリー'

    def get_queryset(self):
        queryset = Category.objects \
            .annotate(post_count=Count('post', filter=Q(post__is_public=True), distinct=True)).exclude(post_count=0) \
            .annotate(tag_count=Count('tag', filter=Q(tag__post__is_public=True), distinct=True))
        return queryset

""" タグ一覧 """
class TagListView(BaseListView):
    template_name = 'blog/blog_table_tag.html'
    model = Tag
    paginate_by = None
    label = 'タグ'

    def get_queryset(self):
        queryset = Tag.objects.select_related('category') \
            .annotate(count=Count('post', filter=Q(post__is_public=True), distinct=True)).order_by('-count', 'name').exclude(count=0)
        return queryset

""" 記事詳細 """
class PostDetailView(generic.DetailView):
    template_name = 'blog/blog_detail.html'
    model = Post

    def get_object(self, queryset=None):
        queryset = Post.objects.select_related('category').prefetch_related('tag')
        post = super().get_object(queryset=queryset)
        if post.is_public or self.request.user.is_authenticated:
            return post 
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context.get('object')
        context['related_posts'] = post.related_posts.select_related('category').prefetch_related('tag').filter(is_public=True)
        context['related_tags'] = post.tag.all().select_related('category')
        context['related_links'] = post.link_set.all().prefetch_related('post')
        context['label'] = post.title
        try:
            context['prev'] = post.get_previous_by_published_at(is_public=True)
        except Post.DoesNotExist:
            context['prev'] = None
        try:
            context['next'] = post.get_next_by_published_at(is_public=True)
        except Post.DoesNotExist:
            context['next'] = None
        return context

""" このサイトについて """
class AboutSiteView(BaseListView):
    template_name = 'blog/blog_single_about.html'
    model = AboutSite
    label = 'このサイトについて'

""" プライバシーポリシー """
class PrivacyPolicyView(BaseListView):
    template_name = 'blog/blog_single_policy.html'
    model = PrivacyPolicy
    label = 'プライバシーポリシー'

""" スニペット """
class SnippetView(LoginRequiredMixin, BaseListView):

    template_name = 'blog/blog_single_snippet.html'
    model = Snippet
    paginate_by = None
    label = 'スニペット'

    def get_queryset(self):
        queryset = Snippet.objects.all().order_by('index')
        return queryset

""" Ping送信 """
@login_required
def ping(request):
    try:
        url = reverse_lazy('blog:sitemap')
        ping_google(sitemap_url=url)
    except Exception:
        raise
    else:
        return redirect('blog:index', permanent=True)

""" 問い合わせフォーム """
class ContactFormView(SuccessMessageMixin, generic.edit.FormView):
    template_name = 'blog/blog_single_contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('blog:contact')
    success_message = "メール送信が完了しました。"
    label = 'お問い合わせ'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = self.label
        return context