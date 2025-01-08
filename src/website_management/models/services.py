from django.db import models

from ..models.seo import SEOModel
from ...core.utils import get_upload_path


class ServicesPage(SEOModel):
    pass


class ServicesPageBlock(models.Model):
    image = models.ImageField(upload_to=get_upload_path)
    title = models.CharField()
    description = models.TextField()