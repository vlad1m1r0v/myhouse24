from django.views.generic import TemplateView

from src.website_management.forms import AdminMainPageSlideFormSet, AdminMainPageForm, AdminMainPageBlockFormSet
from src.website_management.models import MainPageSlide, MainPage, MainPageBlock


class MainPageView(TemplateView):
    template_name = 'website_management/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['slides'] = AdminMainPageSlideFormSet(
        queryset=MainPageSlide.objects.all(),
            prefix='slides',
        )

        context['main_page'] = AdminMainPageForm(instance=MainPage.objects.first())

        context['blocks'] = AdminMainPageBlockFormSet(
            queryset=MainPageBlock.objects.all(),
            prefix='blocks',
        )

        return context