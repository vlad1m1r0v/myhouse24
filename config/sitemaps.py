from django.contrib.sitemaps import Sitemap
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['website_home', 'website_about_us', 'website_services', 'website_tariffs', 'website_contacts']

    def location(self, item):
        return reverse(item)


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        f"Disallow: /adminlte/ \n",
        f"Host: {request.build_absolute_uri(reverse('website_home'))} \n"
        f"Sitemap: {request.build_absolute_uri(reverse('django.contrib.sitemaps.views.sitemap'))}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")