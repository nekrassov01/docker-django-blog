# Generated by Django 3.1 on 2020-08-15 11:53

import blog.models
import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.CharField(default=blog.models.Base.get_str_uuid, editable=False, max_length=33, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日')),
                ('index', models.IntegerField(blank=True, null=True, verbose_name='並び順')),
                ('name', models.CharField(max_length=255, verbose_name='カテゴリ名')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, verbose_name='スラッグ')),
                ('description', models.TextField(blank=True, null=True, verbose_name='説明')),
            ],
            options={
                'verbose_name': 'カテゴリー',
                'verbose_name_plural': 'カテゴリー',
                'db_table': 'category',
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.CharField(default=blog.models.Base.get_str_uuid, editable=False, max_length=33, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日')),
                ('index', models.IntegerField(blank=True, null=True, verbose_name='並び順')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='名前')),
                ('text', models.TextField(blank=True, null=True, verbose_name='内容')),
            ],
            options={
                'verbose_name': 'スニペット',
                'verbose_name_plural': 'スニペット',
                'db_table': 'snippet',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.CharField(default=blog.models.Base.get_str_uuid, editable=False, max_length=33, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日')),
                ('name', models.CharField(max_length=255, verbose_name='タグ名')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, verbose_name='スラッグ')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category', verbose_name='親カテゴリー')),
            ],
            options={
                'verbose_name': 'タグ',
                'verbose_name_plural': 'タグ',
                'db_table': 'tag',
                'ordering': ['name', 'slug'],
            },
        ),
        migrations.CreateModel(
            name='SiteDetail',
            fields=[
                ('id', models.CharField(default=blog.models.Base.get_str_uuid, editable=False, max_length=33, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日')),
                ('keyword', models.TextField(blank=True, default='AWS,PowerShell,Windows,Linux,Python,Django,Docker,インフラ,クラウド,プログラミング,技術,システム管理,自動化', null=True, verbose_name='メタキーワード')),
                ('description', models.TextField(blank=True, default='技術ブログ。学んだ技術のノートや雑記等の置き場所です。AWS,PowerShell,Windows,Linux,Python,Django,Dockerなどが多め。', null=True, verbose_name='メタデスクリプション')),
                ('google_analytics_html', models.TextField(blank=True, verbose_name='Google Analitics')),
                ('google_adsence_html', models.TextField(blank=True, verbose_name='Google AdSense')),
                ('github', models.CharField(blank=True, max_length=255, verbose_name='Github URL')),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='sites.site', verbose_name='サイト')),
            ],
            options={
                'verbose_name': 'サイト詳細',
                'verbose_name_plural': 'サイト詳細',
                'db_table': 'sitedetail',
            },
        ),
        migrations.CreateModel(
            name='PrivacyPolicy',
            fields=[
                ('id', models.CharField(default=blog.models.Base.get_str_uuid, editable=False, max_length=33, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日')),
                ('text', models.TextField(blank=True, null=True, verbose_name='本文')),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='sites.site', verbose_name='サイト')),
            ],
            options={
                'verbose_name': 'プライバシーポリシー',
                'verbose_name_plural': 'プライバシーポリシー',
                'db_table': 'privacy_policy',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.CharField(default=blog.models.Base.get_str_uuid, editable=False, max_length=33, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日')),
                ('is_public', models.BooleanField(default=False, verbose_name='公開フラグ')),
                ('published_at', models.DateTimeField(default=datetime.datetime(1969, 12, 31, 15, 0, tzinfo=utc), help_text='Nullを回避するため、公開フラグをFalseで保存した場合はダミー日時がセットされます。その後、公開したときに日時が上書きされます。', verbose_name='投稿日')),
                ('title', models.CharField(max_length=128, verbose_name='タイトル')),
                ('eyecatch', models.ImageField(blank=True, default='image/post/default/default.webp', null=True, upload_to='image/post/eyecatch/%Y/%m/%d/', verbose_name='アイキャッチ画像')),
                ('description', models.TextField(blank=True, null=True, verbose_name='説明')),
                ('text', models.TextField(blank=True, null=True, verbose_name='本文')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category', verbose_name='カテゴリー')),
                ('related_posts', models.ManyToManyField(blank=True, related_name='_post_related_posts_+', to='blog.Post', verbose_name='関連記事')),
                ('tag', models.ManyToManyField(blank=True, to='blog.Tag', verbose_name='タグ')),
            ],
            options={
                'verbose_name': '記事',
                'verbose_name_plural': '記事',
                'db_table': 'post',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.CharField(default=blog.models.Base.get_str_uuid, editable=False, max_length=33, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日')),
                ('link', models.URLField(blank=True, help_text='URLを指定してください', max_length=255, verbose_name='URL')),
                ('description', models.TextField(blank=True, null=True, verbose_name='説明')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.post', verbose_name='記事')),
            ],
            options={
                'verbose_name': '参考リンク',
                'verbose_name_plural': '参考リンク',
                'db_table': 'link',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.CharField(default=blog.models.Base.get_str_uuid, editable=False, max_length=33, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日')),
                ('title', models.CharField(blank=True, help_text='画像のalt属性として利用されます', max_length=255, verbose_name='タイトル')),
                ('image', models.ImageField(blank=True, default='image/post/default/default.webp', help_text='保存後、本文挿入用HTMLを生成します', null=True, upload_to='image/post/text/%Y/%m/%d/', verbose_name='画像')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.post', verbose_name='記事')),
            ],
            options={
                'verbose_name': '画像',
                'verbose_name_plural': '画像',
                'db_table': 'image',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='AboutSite',
            fields=[
                ('id', models.CharField(default=blog.models.Base.get_str_uuid, editable=False, max_length=33, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日')),
                ('author_image', models.ImageField(blank=True, default='image/site/author_image/author_image.webp', null=True, upload_to='image/site/author_image/', verbose_name='管理者のイメージ')),
                ('site_image', models.ImageField(blank=True, default='image/site/site_image/site_image.webp', null=True, upload_to='image/site/site_image/', verbose_name='サイトのイメージ')),
                ('author_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='管理者の名前')),
                ('author_text', models.TextField(blank=True, null=True, verbose_name='管理者の説明')),
                ('site_text', models.TextField(blank=True, null=True, verbose_name='サイトの説明')),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='sites.site', verbose_name='サイト')),
            ],
            options={
                'verbose_name': 'このサイトについて',
                'verbose_name_plural': 'このサイトについて',
                'db_table': 'about_site',
            },
        ),
    ]
