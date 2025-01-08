from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from src.website_management.forms import AdminServicesPageForm, AdminServicesPageBlockFormSet
from src.website_management.models import ServicesPage, ServicesPageBlock
from .mixin import WebsitePermissionRequiredMixin

class AdminServicesPageView(WebsitePermissionRequiredMixin,
                            TemplateView):
    template_name = 'website_management/adminlte/services.html'

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
        return redirect(reverse_lazy('adminlte:website-management:services'))