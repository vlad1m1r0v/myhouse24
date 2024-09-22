from django.views.generic import TemplateView

from src.website_management.models import AboutUsPage, AboutUsDocument, AboutUsAdditionalGallery, AboutUsGallery


class WebsiteAboutUsView(TemplateView):
    template_name = 'website/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page'] = AboutUsPage.objects.first()
        context['gallery'] = AboutUsGallery.objects.all()
        context['documents'] = AboutUsDocument.objects.all()
        context['additional_gallery'] = AboutUsAdditionalGallery.objects.all()

        return context