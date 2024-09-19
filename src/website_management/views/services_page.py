from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from src.website_management.forms import AdminServicesPageForm, AdminServicesPageBlockFormSet
from src.website_management.models import ServicesPage, ServicesPageBlock


class AdminServicesPageView(PermissionRequiredMixin, TemplateView):
    template_name = 'website_management/services_page.html'
    permission_required = ('authentication.website_management',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        (obj,_) = ServicesPage.objects.get_or_create(pk=1)
        context['page'] = AdminServicesPageForm(instance=obj)

        context['services']  =AdminServicesPageBlockFormSet(
            queryset=ServicesPageBlock.objects.all(),
        )

        return context

    def post(self,request, *args, **kwargs):
        form = AdminServicesPageForm(request.POST, instance=ServicesPage.objects.first())
        services = AdminServicesPageBlockFormSet(request.POST, request.FILES)

        if form.is_valid() and services.is_valid():
            form.save()
            services.save()
            messages.success(request, 'Сторінка "Послуги" успішно оновлена')
        else:
            for form_errors in services.errors:
                for error_list in form_errors.values():
                    for error in error_list:
                        messages.error(self.request, error)
        return redirect(reverse_lazy('adminlte_website_management_services'))

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до управління cайтом')
        logout(self.request)
        return redirect(reverse('authentication_adminlte_login'))