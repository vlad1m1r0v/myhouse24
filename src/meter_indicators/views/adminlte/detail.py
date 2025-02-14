from django.views.generic import DetailView

from .mixin import (
    HouseUserRequiredMixin,
    MeterIndicatorPermissionRequiredMixin
)
from ...models import MeterIndicator


class AdminMeterIndicatorsDetailView(
    HouseUserRequiredMixin,
    MeterIndicatorPermissionRequiredMixin,
    DetailView,
):
    template_name = 'meter_indicators/adminlte/detail.html'
    model = MeterIndicator

    def get_queryset(self):
        return (super().get_queryset()
                .select_related('service', 'service__unit', 'house', 'section', 'flat', 'flat__owner'))
