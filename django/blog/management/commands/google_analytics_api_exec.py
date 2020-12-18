from django.core.management.base import BaseCommand
from blog.models import PopularPost
from .google_analytics_api import get_popular

""" API呼び出し """
class Command(BaseCommand): 
    def handle(self, *args, **options):
        PopularPost.objects.all().delete()
        for link, title, page_view in get_popular():
            try:
                PopularPost.objects.create(link=link, title=title, page_view=page_view)
            except:
                pass