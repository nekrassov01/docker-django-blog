from django.core.management.base import BaseCommand
from blog.models import PopularPost
from .google_analytics_api import get_10_popular

""" API呼び出し """
class Command(BaseCommand): 
    def handle(self, *args, **options):
        PopularPost.objects.all().delete()
        for url, title, page_view in get_10_popular():
            PopularPost.objects.create(url=url, title=title, page_view=page_view)