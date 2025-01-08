from django.views.generic import TemplateView

from src.website_management.models import MainPage, MainPageSlide, MainPageBlock


class WebsiteHomeView(TemplateView):
    template_name = 'website_management/website/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page'] = MainPage.objects.first()
        context['slides'] = MainPageSlide.objects.all()
        context['blocks'] = MainPageBlock.objects.all()

        return context