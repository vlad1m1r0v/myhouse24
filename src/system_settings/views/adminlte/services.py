from django.contrib import messages
from django.db.models import Exists, OuterRef
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from src.system_settings.forms import AdminMeasurementUnitFormSet, AdminServiceFormSet
from src.system_settings.models import MeasurementUnit, Service, TariffService
from src.core.utils import CustomPermissionRequiredMixin


class ServicePermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.services'
    permission_denied_message = 'У Вас немає доступу до послуг'


class AdminServicesView(ServicePermissionRequiredMixin, TemplateView):
    template_name = 'system_settings/adminlte/services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['unit_formset'] = AdminMeasurementUnitFormSet(
            queryset=MeasurementUnit.objects.annotate(
                can_delete=~Exists(
                    Service.objects.filter(unit_id=OuterRef('pk'))
                )
            ),
            prefix='unit'
        )

        context['service_formset'] = AdminServiceFormSet(
            queryset=Service.objects.annotate(
                can_delete=~Exists(
                    TariffService.objects.filter(service_id=OuterRef('pk'))
                )
            ),
            prefix='service'
        )

        return context

    def post(self, *args, **kwargs):
        unit_formset = AdminMeasurementUnitFormSet(self.request.POST, prefix='unit')
        service_formset = AdminServiceFormSet(self.request.POST, prefix='service')

        if unit_formset.is_valid() and service_formset.is_valid():
            unit_formset.save()
            service_formset.save()
            messages.success(self.request, 'Послуги і одиниці вимірювання успішно оновлено')
        else:
            for form_errors in unit_formset.errors:
                for error_list in form_errors.values():
                    for error in error_list:
                        messages.error(self.request, error)

            for form_errors in service_formset.errors:
                for error_list in form_errors.values():
                    for error in error_list:
                        messages.error(self.request, error)

        return redirect(reverse('adminlte:system-settings:services:index'))
