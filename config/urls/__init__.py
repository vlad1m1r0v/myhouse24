from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from config.sitemaps import StaticViewSitemap, robots_txt

sitemaps = {
    'static': StaticViewSitemap,
}
urlpatterns = [
    path('', include('config.urls.authentication')),
    path('', include('config.urls.adminlte')),
    path('', include('config.urls.website')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# sitemap and robots
urlpatterns += [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
]

urlpatterns += debug_toolbar_urls()