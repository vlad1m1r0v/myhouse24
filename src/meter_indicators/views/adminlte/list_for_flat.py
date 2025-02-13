from django.views.generic import TemplateView

from src.flats.models import Flat
from .mixin import (
    MeterIndicatorPermissionRequiredMixin,
    HouseUserRequiredMixin
)


class AdminMeterIndicatorsListForFlatView(
    HouseUserRequiredMixin,
    MeterIndicatorPermissionRequiredMixin,
    TemplateView
):
    template_name = 'meter_indicators/adminlte/list_for_flat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        flat_id = self.request.GET.get('flat_id')
        flat = Flat.objects.get(pk=flat_id)
        context['flat'] = flat

        return context
