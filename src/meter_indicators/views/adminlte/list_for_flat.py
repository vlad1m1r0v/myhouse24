from django.views.generic import TemplateView

from src.flats.models import Flat
from src.system_settings.models import Service
from .mixin import (
    MeterIndicatorPermissionRequiredMixin,
    HouseUserRequiredMixin
)
from ...forms import AdminMeterIndicatorsForFlatFiltersForm


class AdminMeterIndicatorsListForFlatView(
    HouseUserRequiredMixin,
    MeterIndicatorPermissionRequiredMixin,
    TemplateView
):
    template_name = 'meter_indicators/adminlte/list_for_flat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form_initials = {}

        flat_id = self.request.GET.get('flat_id')
        flat = Flat.objects.get(pk=flat_id)
        context['flat'] = flat

        service_id = self.request.GET.get('service_id')
        if service_id:
            service = Service.objects.select_related('unit').get(pk=service_id)
            form_initials['service'] = service

        context['filters'] = AdminMeterIndicatorsForFlatFiltersForm(
            initial=form_initials,
        )

        return context
