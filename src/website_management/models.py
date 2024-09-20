import os

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


class ServicesPage(SEOModel):
    pass


class ServicesPageBlock(models.Model):
    image = models.ImageField(upload_to=get_upload_path)
    title = models.CharField()
    description = models.TextField()


class TariffsPage(SEOModel):
    title = models.CharField()
    description = models.TextField()


class TariffsPageBlock(models.Model):
    image = models.ImageField(upload_to=get_upload_path)
    title = models.CharField()


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