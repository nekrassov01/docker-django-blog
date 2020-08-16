import os
import pytz
import uuid as uuid
from urllib.parse import urlparse
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone

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
        ordering = ['name', 'slug']

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
    category = models.ForeignKey(Category, verbose_name='カテゴリー', null=True, blank=True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)
    related_posts = models.ManyToManyField('self', verbose_name='関連記事', blank=True)
    eyecatch = models.ImageField(verbose_name='アイキャッチ画像', upload_to='image/post/eyecatch/%Y/%m/%d/', null=True, blank=True)
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
        return '{}: {}'.format(self.category, self.title)

""" 画像 | 記事の本文で利用 """
class Image(Base):
    class Meta:
        db_table = 'image'
        verbose_name = '画像'
        verbose_name_plural = '画像'
        ordering = ['created_at']

    post = models.ForeignKey(Post, verbose_name='記事', on_delete=models.PROTECT)
    title = models.CharField('タイトル', max_length=255, blank=True, help_text='画像のalt属性として利用されます')
    image = models.ImageField(verbose_name='画像', upload_to='image/post/text/%Y/%m/%d/', null=True, blank=True, help_text='保存後、本文挿入用HTMLを生成します')

    def __str__(self):
        return '本文挿入用HTML: <img src="" data-src="{}" class="lozad py-3 w-100" alt="{}">'.format(self.image.url, self.title)

""" 外部リンク | 記事の本文で利用 """
class Link(Base):
    class Meta:
        db_table = 'link'
        verbose_name = '参考リンク'
        verbose_name_plural = '参考リンク'
        ordering = ['created_at']

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
    keyword = models.TextField(verbose_name='メタキーワード', blank=True, null=True, default='AWS,PowerShell,Windows,Linux,Python,Django,Docker,インフラ,クラウド,プログラミング,技術,システム管理,自動化')
    description = models.TextField(verbose_name='メタデスクリプション', blank=True, null=True, default='技術ブログ。学んだ技術のノートや雑記等の置き場所です。AWS,PowerShell,Windows,Linux,Python,Django,Dockerなどが多め。')
    google_analytics_html = models.TextField(verbose_name='Google Analitics', blank=True)
    google_adsence_html = models.TextField(verbose_name='Google AdSense', blank=True)
    github = models.CharField(verbose_name='Github URL', max_length=255, blank=True)

    def __str__(self):
        return '「{}」の基本情報を編集します。'.format(self.site.name)

""" このサイトについて | サイトのインラインで利用 """
class AboutSite(Base):
    class Meta:
        db_table = 'about_site'
        verbose_name = 'このサイトについて'
        verbose_name_plural = 'このサイトについて'

    site = models.OneToOneField(Site, verbose_name='サイト', on_delete=models.PROTECT)
    author_image = models.ImageField(verbose_name='管理者のイメージ', upload_to='image/site/author_image/', blank=True, null=True)
    site_image = models.ImageField(verbose_name='サイトのイメージ', upload_to='image/site/site_image/', blank=True, null=True)
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

""" 本文編集用スニペット """
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
