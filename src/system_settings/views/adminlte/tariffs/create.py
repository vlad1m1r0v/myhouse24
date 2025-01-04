from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from src.system_settings.forms import AdminTariffForm, AdminTariffServiceFormSet
from src.system_settings.models import Tariff
from .mixin import TariffPermissionRequiredMixin


class AdminTariffCreateView(TariffPermissionRequiredMixin,
                            TemplateView):
    template_name = 'adminlte/system_settings/tariffs/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tariff_id = self.request.GET.get('tariff_id', None)

        if tariff_id:
            tariff = Tariff.objects.get(pk=tariff_id)

            form = AdminTariffForm(
                initial={
                    'name': tariff.name,
                    'description': tariff.description
                },
                instance=tariff)
            formset = AdminTariffServiceFormSet(
                instance=tariff,
                prefix='service',
            )
        else:
            form = AdminTariffForm()
            formset = AdminTariffServiceFormSet(prefix='service')

        context['tariff'] = form
        context['services'] = formset

        return context

    def post(self, *args, **kwargs):
        form = AdminTariffForm(self.request.POST)
        formset = AdminTariffServiceFormSet(self.request.POST, prefix='service')

        if form.is_valid() and formset.is_valid():
            tariff = form.save()
            formset.instance = tariff
            formset.save()

            messages.success(self.request, 'Тариф успішно створено')
            return redirect(reverse('adminlte:system-settings:tariffs:list'))
        else:
            for form_errors in formset.errors:
                for error_list in form_errors.values():
                    for error in error_list:
                        messages.error(self.request, error)

            return self.render_to_response(self.get_context_data(tariff=form, services=formset))