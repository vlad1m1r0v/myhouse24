from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from src.system_settings.forms import AdminTariffForm, AdminTariffServiceFormSet
from src.system_settings.models import Tariff
from .mixin import TariffPermissionRequiredMixin


class AdminTariffUpdateView(TariffPermissionRequiredMixin,
                            TemplateView):
    template_name = 'system_settings/adminlte/tariffs/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tariff = Tariff.objects.get(pk=self.kwargs['pk'])

        context['tariff'] = AdminTariffForm(instance=tariff)
        context['services'] = AdminTariffServiceFormSet(
            instance=tariff,
            prefix='service'
        )

        return context

    def post(self, *args, **kwargs):
        instance = Tariff.objects.get(pk=self.kwargs['pk'])
        tariff = AdminTariffForm(self.request.POST, instance=instance)
        services = AdminTariffServiceFormSet(self.request.POST, instance=instance, prefix='service')

        if tariff.is_valid() and services.is_valid():
            tariff.save()
            services.save()
            messages.success(self.request, 'Інформацію про тариф успішно оновлено')
            return redirect(reverse('adminlte:system-settings:tariffs:list'))
        else:
            for form_errors in services.errors:
                for error_list in form_errors.values():
                    for error in error_list:
                        messages.error(self.request, error)

            return self.render_to_response(self.get_context_data(tariff=tariff, services=services))