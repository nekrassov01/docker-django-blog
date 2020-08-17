from django.core.management.base import BaseCommand
from blog.models import CategoryPost, CategoryTag, TagPost, MonthPost, WordCloud
from .site_report_api import get_category_post_dict, get_category_tag_dict, get_tag_post_dict, get_month_post_list, get_word_dict

""" API呼び出し """
class Command(BaseCommand): 
    def handle(self, *args, **options):

        CategoryPost.objects.all().delete()
        for key, value in get_category_post_dict():
            CategoryPost.objects.create(category=key, post_count=value)
        
        CategoryTag.objects.all().delete()
        for key, value in get_category_tag_dict():
            CategoryTag.objects.create(category=key, tag_count=value)
        
        TagPost.objects.all().delete()
        for key, value in get_tag_post_dict():
            TagPost.objects.create(tag=key, post_count=value)
        
        MonthPost.objects.all().delete()
        for date, category, month_post_count in get_month_post_list():
            MonthPost.objects.create(month=date, category=category, post_count=month_post_count)
        
        WordCloud.objects.all().delete()
        for key, value in get_word_dict():
            WordCloud.objects.create(word=key, word_count=value)