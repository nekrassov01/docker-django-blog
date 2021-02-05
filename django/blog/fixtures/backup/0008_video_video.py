# Generated by Django 3.1.6 on 2021-02-04 16:15

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_remove_video_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video',
            field=cloudinary.models.CloudinaryField(blank=True, help_text='保存後、本文挿入用HTMLを生成します', max_length=255, null=True, verbose_name='動画'),
        ),
    ]
