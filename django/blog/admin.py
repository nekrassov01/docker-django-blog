from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
from django.urls import path
from django.template.response import TemplateResponse
from django_summernote.admin import SummernoteModelAdmin, SummernoteInlineModelAdmin
from .models import Base, Post, Category, Tag, SiteDetail, AboutSite, PrivacyPolicy, Snippet, Image, Video, Link, PopularPost, CategoryPost, CategoryTag, TagPost, MonthPost, WordCloud

class SiteDetailInline(admin.StackedInline):
    model = SiteDetail
    readonly_fields = ('created_at', 'updated_at')

class AboutSiteInline(admin.StackedInline, SummernoteInlineModelAdmin):
    model = AboutSite
    readonly_fields = ('created_at', 'updated_at')
    summernote_fields = ('site_text', 'author_text')

class PrivacyPolicyInline(admin.StackedInline, SummernoteInlineModelAdmin):
    model = PrivacyPolicy
    readonly_fields = ('created_at', 'updated_at')
    summernote_fields = ('text')

class SiteAdmin(admin.ModelAdmin):
    model = Site
    inlines = [SiteDetailInline, AboutSiteInline, PrivacyPolicyInline]
    list_display = ('id', 'domain', 'name')

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('id', 'created_at', 'updated_at', 'index', 'name', 'slug', 'description')
    ordering = ('index',)
    search_fields = ('name',)
    readonly_fields = ('id', 'created_at', 'updated_at')

class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('id', 'created_at', 'updated_at', 'category', 'name', 'slug')
    ordering = ('category', 'slug')
    list_filter = ('category',)
    search_fields = ('name',)
    readonly_fields = ('id', 'created_at', 'updated_at')

class SnippetAdmin(admin.ModelAdmin):
    model = Snippet
    list_display = ('id', 'created_at', 'updated_at', 'index', 'name', 'truncate_text')
    ordering = ('index',)
    search_fields = ('name',)
    readonly_fields = ('id', 'created_at', 'updated_at')

    def truncate_text(self, obj):
        count = 150
        if len(obj.text) <= count:
            return obj.text
        else:
            return obj.text[:count] + '…'
    
    truncate_text.short_description = '内容'

class ImageInline(admin.StackedInline):
    model = Image
    ordering = ('index',)
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

class VideoInline(admin.StackedInline):
    model = Video
    ordering = ('index',)
    extra = 1
    readonly_fields = ('id', 'created_at', 'updated_at')

class LinkInline(admin.StackedInline):
    model = Link
    ordering = ('index',)
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

class PostAdmin(SummernoteModelAdmin):
    model = Post
    inlines = [ImageInline, VideoInline, LinkInline]
    list_display = ('is_public', 'id', 'created_at', 'updated_at', 'published_at', 'category', 'title', 'subtitle', 'truncate_desc', 'preview')
    list_display_links = ('id', 'preview')
    ordering = ('-created_at',)
    list_filter = ('is_public', 'category')
    search_fields = ('title', 'text')
    filter_horizontal = ('tag', 'related_posts')
    summernote_fields = ('text')
    actions = ['bulk_publish', 'bulk_unpublish']
    readonly_fields = ('id', 'created_at', 'updated_at')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'tag':
            kwargs['queryset'] = Tag.objects.order_by('category__index', 'slug')
        if db_field.name == "related_posts":
            kwargs['queryset'] = Post.objects.order_by('category__index', 'title')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def preview(self, obj):
        return mark_safe('<img src="{}" style="width:120px;height:auto;">'.format(obj.eyecatch.url))

    def truncate_desc(self, obj):
        count = 48
        if len(obj.description) <= count:
            return obj.description
        else:
            return obj.description[:count] + '…'           

    def bulk_publish(self, request, queryset):
        queryset.update(is_public=True)

    def bulk_unpublish(self, request, queryset):
        queryset.update(is_public=False)

    truncate_desc.short_description = '説明'
    preview.short_description = 'プレビュー'
    preview.allow_tags = True
    bulk_publish.short_description = '選択された 記事 を公開扱いにする'
    bulk_unpublish.short_description = '選択された 記事 を非公開扱いにする'

class PopularPostAdmin(admin.ModelAdmin):
    model = PopularPost
    list_display = ('id', 'created_at', 'updated_at', 'title', 'link', 'page_view')
    ordering = ('-page_view',)
    readonly_fields = ('id', 'created_at', 'updated_at')

class CategoryPostAdmin(admin.ModelAdmin):
    model = CategoryPost
    list_display = ('id', 'created_at', 'updated_at', 'category', 'post_count')
    ordering = ('-post_count',)
    readonly_fields = ('id', 'created_at', 'updated_at')

class CategoryTagAdmin(admin.ModelAdmin):
    model = CategoryTag
    list_display = ('id', 'created_at', 'updated_at', 'category', 'tag_count')
    ordering = ('-tag_count',)
    readonly_fields = ('id', 'created_at', 'updated_at')

class TagPostAdmin(admin.ModelAdmin):
    model = TagPost
    list_display = ('id', 'created_at', 'updated_at', 'tag', 'post_count')
    ordering = ('-post_count',)
    readonly_fields = ('id', 'created_at', 'updated_at')

class MonthPostAdmin(admin.ModelAdmin):
    model = MonthPost
    list_display = ('id', 'created_at', 'updated_at', 'month', 'category', 'post_count')
    ordering = ('month', 'category', 'post_count',)
    readonly_fields = ('id', 'created_at', 'updated_at')

class WordCloudAdmin(admin.ModelAdmin):
    model = WordCloud
    list_display = ('id', 'created_at', 'updated_at', 'word', 'word_count')
    ordering = ('-word_count',)
    readonly_fields = ('id', 'created_at', 'updated_at')

admin.autodiscover()
admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin) 
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Snippet, SnippetAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PopularPost, PopularPostAdmin)
admin.site.register(CategoryPost, CategoryPostAdmin)
admin.site.register(CategoryTag, CategoryTagAdmin)
admin.site.register(TagPost, TagPostAdmin)
admin.site.register(MonthPost, MonthPostAdmin)
admin.site.register(WordCloud, WordCloudAdmin)