from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView

from .mixin import (
    SuccessUrlMixin,
    MeterIndicatorPermissionRequiredMixin,
    HouseUserRequiredMixin
)
from ...forms import AdminMeterIndicatorForm
from ...models import MeterIndicator


class AdminMeterIndicatorsUpdateView(
    SuccessUrlMixin,
    SuccessMessageMixin,
    HouseUserRequiredMixin,
    MeterIndicatorPermissionRequiredMixin,
    UpdateView
):
    model = MeterIndicator
    form_class = AdminMeterIndicatorForm
    template_name = 'meter_indicators/adminlte/update.html'
    success_message = 'Показник рахунку успішно оновлено'
