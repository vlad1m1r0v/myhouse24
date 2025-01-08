from django.core.paginator import Paginator
from django.views.generic import TemplateView

from src.website_management.models import ServicesPage, ServicesPageBlock


class WebsiteServicesView(TemplateView):
    template_name = 'website_management/website/services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page'] = ServicesPage.objects.first()

        services = ServicesPageBlock.objects.all()
        paginator = Paginator(services, per_page=10)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context