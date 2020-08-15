# Generated by Django 3.0.8 on 2020-07-24 04:33

from django.core.management import call_command
from django.db import migrations


def load_fixture(apps, schema_editor):
    call_command('loaddata', 'blog/fixtures/blog.json', app_label='blog')


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]