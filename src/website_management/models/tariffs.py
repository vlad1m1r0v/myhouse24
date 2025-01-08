from django.db import models

from ..models.seo import SEOModel
from ...core.utils import get_upload_path


class TariffsPage(SEOModel):
    title = models.CharField()
    description = models.TextField()


class TariffsPageBlock(models.Model):
    image = models.ImageField(upload_to=get_upload_path)
    title = models.CharField()