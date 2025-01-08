from django.db import models

from ..models.seo import SEOModel


class ContactsPage(SEOModel):
    title = models.CharField()
    description = models.TextField()
    website_link =models.URLField()
    map_iframe = models.TextField()
    name = models.CharField()
    location = models.CharField()
    address = models.CharField()
    phone = models.CharField()
    email = models.EmailField()