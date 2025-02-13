from django.views.generic import TemplateView

from .mixin import MeterIndicatorPermissionRequiredMixin


class AdminMeterIndicatorsListView(
    MeterIndicatorPermissionRequiredMixin,
    TemplateView
):
    template_name = 'meter_indicators/adminlte/list.html'