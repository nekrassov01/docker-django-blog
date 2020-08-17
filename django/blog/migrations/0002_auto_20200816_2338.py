# Generated by Django 2.2 on 2020-08-16 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PopularPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='タイトル')),
                ('link', models.URLField(max_length=255, verbose_name='URL')),
                ('page_view', models.IntegerField(verbose_name='ページビュー')),
            ],
            options={
                'verbose_name': '人気記事',
                'verbose_name_plural': '人気記事',
                'db_table': 'popular_post',
            },
        ),
        migrations.AlterField(
            model_name='aboutsite',
            name='author_image',
            field=models.ImageField(blank=True, null=True, upload_to='image/site/author_image/', verbose_name='管理者のイメージ'),
        ),
        migrations.AlterField(
            model_name='aboutsite',
            name='site_image',
            field=models.ImageField(blank=True, null=True, upload_to='image/site/site_image/', verbose_name='サイトのイメージ'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, help_text='保存後、本文挿入用HTMLを生成します', null=True, upload_to='image/post/text/%Y/%m/%d/', verbose_name='画像'),
        ),
        migrations.AlterField(
            model_name='post',
            name='eyecatch',
            field=models.ImageField(blank=True, null=True, upload_to='image/post/eyecatch/%Y/%m/%d/', verbose_name='アイキャッチ画像'),
        ),
    ]
