import os

from django.db import models

from ..models.seo import SEOModel
from ...core.utils import get_upload_path


class AboutUsPage(SEOModel):
    director_photo = models.ImageField(upload_to=get_upload_path)
    title = models.CharField()
    description = models.TextField()
    additional_title = models.CharField()
    additional_description = models.TextField()


class AboutUsGallery(models.Model):
    image = models.ImageField(upload_to=get_upload_path)


class AboutUsAdditionalGallery(models.Model):
    image = models.ImageField(upload_to=get_upload_path)


class AboutUsDocument(models.Model):
    title = models.CharField()
    file = models.FileField(upload_to=get_upload_path)

    def extension(self):
        name, rest = os.path.splitext(self.file.name)
        return rest[1:]