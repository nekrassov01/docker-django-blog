import os
import pytz
import uuid
from urllib.parse import urlparse
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django_cleanup import cleanup
from cloudinary.models import CloudinaryField

""" ベース | 基底クラス """
class Base(models.Model):
    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']

    """ uuidからハイフンを削除して文字列化 """
    def get_str_uuid():
        return uuid.uuid4().hex

    id = models.CharField(primary_key=True, default=get_str_uuid, max_length=33, editable=False, unique=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True, null=True)

""" カテゴリ | Postと1対多で紐づく """
class Category(Base):
    class Meta:
        db_table = 'category'
        verbose_name = 'カテゴリー'
        verbose_name_plural = 'カテゴリー'
        ordering = ['index']

    index = models.IntegerField(verbose_name='並び順', null=True, blank=True)
    name = models.CharField(verbose_name='カテゴリ名', max_length=255)
    slug = models.SlugField(verbose_name='スラッグ', max_length=255, null=True, blank=True)
    description = models.TextField(verbose_name='説明', blank=True, null=True)

    def __str__(self):
        return '{}: {}'.format(self.index, self.name)

""" タグ | Postと多対多で紐づく """
class Tag(Base):
    class Meta:
        db_table = 'tag'
        verbose_name = 'タグ'
        verbose_name_plural = 'タグ'
        ordering = ['category', 'slug']

    name = models.CharField(verbose_name='タグ名', max_length=255)
    slug = models.SlugField(verbose_name='スラッグ', max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name='親カテゴリー', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '{}: {}'.format(self.category, self.name)

""" 記事 | メイン """
class Post(Base):
    class Meta:
        db_table = 'post'
        verbose_name = '記事'
        verbose_name_plural = '記事'
        ordering = ['-created_at']

    """ ダミー日時の指定 """
    default_datetime = timezone.make_aware(timezone.datetime(year=1970, month=1, day=1, hour=0))

    is_public = models.BooleanField(verbose_name='公開フラグ', default=False)
    published_at = models.DateTimeField(verbose_name='投稿日', default=default_datetime, help_text='Nullを回避するため、公開フラグをFalseで保存した場合はダミー日時がセットされます。その後、公開したときに日時が上書きされます。')
    title = models.CharField(verbose_name='タイトル', max_length=128)
    subtitle = models.CharField(verbose_name='サブタイトル', max_length=128, null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name='カテゴリー', null=True, blank=True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)
    related_posts = models.ManyToManyField('self', verbose_name='関連記事', blank=True)
    eyecatch = CloudinaryField(verbose_name='アイキャッチ画像', null=True, blank=True, overwrite=True, resource_type="auto", folder="media/image/eyecatch", tags="EyeCatch")
    description = models.TextField(verbose_name='説明', blank=True, null=True)
    text = models.TextField(verbose_name='本文', blank=True, null=True)

    """ 投稿日をセット """
    def save(self, *args, **kwargs):
        if self.is_public and self.published_at == self.default_datetime:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    """ メタキーワード """
    def get_keyword(self):
        meta_keyword = ','.join(tag.name for tag in self.tag.all())
        return meta_keyword

    def __str__(self):
        if self.subtitle:
            return '{}: {} - {}'.format(self.category, self.title, self.subtitle)
        else:
            return '{}: {}'.format(self.category, self.title)

""" 画像 | 記事の本文で利用 """
class Image(Base):
    class Meta:
        db_table = 'image'
        verbose_name = '画像'
        verbose_name_plural = '画像'
        ordering = ['index']

    index = models.IntegerField(verbose_name='並び順', null=True, blank=True)
    post = models.ForeignKey(Post, verbose_name='記事', on_delete=models.PROTECT)
    title = models.CharField('タイトル', max_length=255, blank=True, help_text='画像のalt属性として利用されます')
    image = CloudinaryField(verbose_name='画像', null=True, blank=True, help_text='保存後、本文挿入用HTMLを生成します', overwrite=True, resource_type="auto", folder="media/image/post/", tags="Post")

    def __str__(self):
        return '本文挿入用HTML: <img src="" data-src="{}" class="lozad w-100" alt="{}">'.format(self.image.url, self.title)

""" 動画 | 記事の本文で利用 """
class Video(Base):
    class Meta:
        db_table = 'video'
        verbose_name = '動画'
        verbose_name_plural = '動画'
        ordering = ['index']

    index = models.IntegerField(verbose_name='並び順', null=True, blank=True)
    post = models.ForeignKey(Post, verbose_name='記事', on_delete=models.PROTECT)
    title = models.CharField('タイトル', max_length=255, blank=True, help_text='動画のalt属性として利用されます')
    video = CloudinaryField(verbose_name='動画', null=True, blank=True, help_text='保存後、本文挿入用HTMLを生成します', overwrite=True, resource_type="auto", folder="media/video/", tags="Video")

    def __str__(self):
        return '本文挿入用HTML: <video controls="" controlslist="nodownload" loop="" preload="none" class="w-100"><source src="{}" alt="{}"></video>'.format(self.video.url, self.title)

""" 外部リンク | 記事の本文で利用 """
class Link(Base):
    class Meta:
        db_table = 'link'
        verbose_name = '参考リンク'
        verbose_name_plural = '参考リンク'
        ordering = ['index']

    index = models.IntegerField(verbose_name='並び順', null=True, blank=True)
    post = models.ForeignKey(Post, verbose_name='記事', on_delete=models.PROTECT)
    link = models.URLField(verbose_name='URL', max_length=255, blank=True, help_text='URLを指定してください')
    description = models.TextField(verbose_name='説明', blank=True, null=True)

    def __str__(self):
        self.domain = urlparse(self.link).netloc
        return 'ドメイン: {} | URL: {}'.format(self.domain, self.link)

""" サイト詳細 | サイトのインラインで利用 """
class SiteDetail(Base):
    class Meta:
        db_table = 'sitedetail'
        verbose_name = 'サイト詳細'
        verbose_name_plural = 'サイト詳細'

    site = models.OneToOneField(Site, verbose_name='サイト', on_delete=models.PROTECT)
    keyword = models.TextField(verbose_name='メタキーワード', blank=True, null=True)
    description = models.TextField(verbose_name='メタデスクリプション', blank=True, null=True)
    google_analytics_html = models.TextField(verbose_name='Google Analitics', blank=True)
    google_adsence_html = models.TextField(verbose_name='Google AdSense', blank=True)
    github = models.CharField(verbose_name='GitHub URL', max_length=255, blank=True)

    def __str__(self):
        return '「{}」の基本情報を編集します。'.format(self.site.name)

""" このサイトについて | サイトのインラインで利用 """
class AboutSite(Base):
    class Meta:
        db_table = 'about_site'
        verbose_name = 'このサイトについて'
        verbose_name_plural = 'このサイトについて'

    site = models.OneToOneField(Site, verbose_name='サイト', on_delete=models.PROTECT)
    author_image = CloudinaryField(verbose_name='管理者のイメージ', null=True, blank=True, overwrite=True, resource_type="auto", folder="media/image/site/", tags="Site")
    site_image = CloudinaryField(verbose_name='サイトのイメージ', null=True, blank=True, overwrite=True, resource_type="auto", folder="media/image/site/", tags="Site")  
    author_name = models.CharField(verbose_name='管理者の名前', max_length=255, blank=True, null=True)
    author_text = models.TextField(verbose_name='管理者の説明', blank=True, null=True)
    site_text = models.TextField(verbose_name='サイトの説明', blank=True, null=True)

    def __str__(self):
        return '「{}」の紹介や管理者の紹介を編集します。'.format(self.site.name)

""" プライバシーポリシー | サイトのインラインで利用 """
class PrivacyPolicy(Base):
    class Meta:
        db_table = 'privacy_policy'
        verbose_name = 'プライバシーポリシー'
        verbose_name_plural = 'プライバシーポリシー'

    site = models.OneToOneField(Site, verbose_name='サイト', on_delete=models.PROTECT)
    text = models.TextField(verbose_name='本文', blank=True, null=True)

    def __str__(self):
        return '「{}」のプライバシーポリシーを編集します。'.format(self.site.name)

""" スニペット | 本文編集用 """
class Snippet(Base):
    class Meta:
        db_table = 'snippet'
        verbose_name = 'スニペット'
        verbose_name_plural = 'スニペット'

    index = models.IntegerField(verbose_name='並び順', null=True, blank=True)
    name = models.CharField(verbose_name='名前', max_length=255, blank=True, null=True)
    text = models.TextField(verbose_name='内容', blank=True, null=True)

    def __str__(self):
        return '{}: {}'.format(self.index, self.name)

""" 人気記事 | Google Analytics Reporting API から取得して格納する """
@cleanup.ignore
class PopularPost(Base):
    class Meta:
        db_table = 'popular_post'
        verbose_name = '人気記事'
        verbose_name_plural = '人気記事'

    title = models.CharField(verbose_name='タイトル', max_length=128)
    link = models.CharField(verbose_name='リンク', max_length=255)
    page_view = models.IntegerField(verbose_name='ページビュー')
    detail_pk = models.CharField(verbose_name='記事のID', max_length=255, null=True, blank=True)
    detail_is_public = models.BooleanField(verbose_name='記事の公開フラグ', default=False)
    detail_published_at = models.DateTimeField(verbose_name='記事の投稿日', null=True, blank=True)
    detail_category = models.CharField(verbose_name='記事のカテゴリー', max_length=255, null=True, blank=True)
    detail_title = models.CharField(verbose_name='記事のタイトル', max_length=255, null=True, blank=True)
    detail_subtitle = models.CharField(verbose_name='記事のサブタイトル', max_length=255, null=True, blank=True)
    detail_eyecatch = CloudinaryField(verbose_name='記事のアイキャッチ画像',null=True, blank=True)

    def save(self, *args, **kwargs):
        post_detail_pk = self.link.split('/')[-2]
        post = Post.objects.get(pk=post_detail_pk)
        self.detail_pk = post.pk
        self.detail_is_public = post.is_public
        self.detail_published_at = post.published_at
        self.detail_category = post.category.name
        self.detail_title = post.title
        self.detail_subtitle = post.subtitle
        self.detail_eyecatch = post.eyecatch
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.title)

""" 自作 Reporting API | 1.カテゴリ別記事数 """
class CategoryPost(Base):
    class Meta:
        db_table = 'category_post'
        verbose_name = 'カテゴリ別: 記事数'
        verbose_name_plural = 'レポート - カテゴリ別: 記事数'

    category = models.CharField(verbose_name='カテゴリ名', max_length=255)
    post_count = models.IntegerField(verbose_name='記事数', null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.category, self.post_count)

""" 自作 Reporting API | 2.カテゴリ別タグ数 """
class CategoryTag(Base):
    class Meta:
        db_table = 'category_tag'
        verbose_name = 'カテゴリ別: タグ数'
        verbose_name_plural = 'レポート - カテゴリ別: タグ数'

    category = models.CharField(verbose_name='カテゴリ名', max_length=255, null=True, blank=True)
    tag_count = models.IntegerField(verbose_name='タグ数', null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.category, self.tag_count)

""" 自作 Reporting API | 3.タグ別記事数 """
class TagPost(Base):
    class Meta:
        db_table = 'tag_post'
        verbose_name = 'タグ別: 記事数'
        verbose_name_plural = 'レポート - タグ別: 記事数'

    tag = models.CharField(verbose_name='タグ名', max_length=255, null=True, blank=True)
    post_count = models.IntegerField(verbose_name='記事数', null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.tag, self.post_count)

""" 自作 Reporting API | 4.月別記事数 """
class MonthPost(Base):
    class Meta:
        db_table = 'month_post'
        verbose_name = 'カテゴリ別: 記事数推移'
        verbose_name_plural = 'レポート - カテゴリ別: 記事数推移'

    month = models.CharField(verbose_name='年月', max_length=255, null=True, blank=True)
    category = models.CharField(verbose_name='タグ名', max_length=255, null=True, blank=True)
    post_count = models.IntegerField(verbose_name='記事数', null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.month, self.category, self.post_count)

""" 自作 Reporting API | 5.ワードクラウド """
class WordCloud(Base):
    class Meta:
        db_table = 'word_cloud'
        verbose_name = 'ワードクラウド'
        verbose_name_plural = 'レポート - ワードクラウド'

    word = models.CharField(verbose_name='ワード', max_length=255, null=True, blank=True)
    word_count = models.IntegerField(verbose_name='出現数', null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.word, self.word_count)