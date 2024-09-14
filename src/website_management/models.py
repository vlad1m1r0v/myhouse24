from django.db import models

from src.core.utils import get_upload_path


class SEOModel(models.Model):
    seo_title = models.CharField()
    seo_keywords = models.CharField()
    seo_description = models.TextField()

    class Meta:
        abstract = True


class MainPage(SEOModel):
    title = models.CharField()
    description = models.TextField()
    show_app_links = models.BooleanField(null=False, default=False)


class MainPageSlide(models.Model):
    image = models.ImageField(upload_to=get_upload_path)

class MainPageBlock(models.Model):
    image = models.ImageField(upload_to=get_upload_path)
    title = models.CharField()
    description = models.TextField()