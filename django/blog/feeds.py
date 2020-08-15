from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.urls import reverse, reverse_lazy
from django.shortcuts import resolve_url
from .models import Post, SiteDetail

class PostFeed(Feed):
    link = reverse_lazy('blog:index')

    @property
    def site(self):
        if not hasattr(self, '_site'):
            site = Site.objects.get(pk=settings.SITE_ID)
            sitedetail, _ = SiteDetail.objects.get_or_create(site=site)
            self._site = sitedetail
        return self._site

    def title(self):
        return self.site.site.name

    def description(self):
        return self.site.description

    def items(self):
        return Post.objects.filter(is_public=True).order_by('-published_at', '-created_at')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return resolve_url('blog:detail', pk=item.pk)
