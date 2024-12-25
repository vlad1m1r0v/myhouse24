"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from config.sitemaps import StaticViewSitemap, robots_txt

sitemaps = {
    'static': StaticViewSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('src.authentication.urls')),
    path('', include('src.system_settings.urls')),
    path('', include('src.website_management.urls')),
    path('', include('src.houses.urls')),
    path('', include('src.flat_owners.urls')),
    path('', include('src.flats.urls')),
    path('', include('src.personal_accounts.urls')),
    path('', include('src.meter_indicators.urls')),
    path('', include('src.master_call_requests.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# sitemap and robots
urlpatterns += [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
]

urlpatterns += debug_toolbar_urls()