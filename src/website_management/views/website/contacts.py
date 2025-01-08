from django.views.generic import TemplateView

from src.website_management.models import ContactsPage


class WebsiteContactsView(TemplateView):
    template_name = 'website_management/website/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page'] = ContactsPage.objects.first()

        return context