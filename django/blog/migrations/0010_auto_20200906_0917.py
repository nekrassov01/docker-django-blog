# Generated by Django 2.2.8 on 2020-09-06 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20200906_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='eyecatch',
            field=models.ImageField(blank=True, default='image/post/eyecatch/default/default.png', null=True, upload_to='image/post/eyecatch/%Y/%m/%d/', verbose_name='アイキャッチ画像'),
        ),
    ]
