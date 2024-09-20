from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from src.website_management.forms import AdminContactsPageForm
from src.website_management.models import ContactsPage


class AdminContactsPageView(PermissionRequiredMixin, TemplateView):
    template_name = 'website_management/contacts_page.html'
    permission_required = ('authentication.website_management',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        (obj,_) = ContactsPage.objects.get_or_create(pk=1)
        context['page'] = AdminContactsPageForm(instance=obj)

        return context

    def post(self, *args, **kwargs):
        page = AdminContactsPageForm(self.request.POST, instance=ContactsPage.objects.first())

        if page.is_valid():
            page.save()
            messages.success(self.request, 'Контактна інформація сайту успішно оновлена')
        else:
            messages.error(self.request, 'Виникли певні помилки про оновленні контактної інформації')

        return redirect(reverse('adminlte_website_management_contacts'))

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до управління cайтом')
        logout(self.request)
        return redirect(reverse('authentication_adminlte_login'))
