from django.db import models
from src.core.utils import get_upload_path
from ..models.seo import SEOModel


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