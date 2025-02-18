from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView

from src.flats.models import Flat
from src.system_settings.models import Service
from .mixin import (
    SuccessUrlMixin,
    MeterIndicatorPermissionRequiredMixin,
    HouseUserRequiredMixin
)
from ...forms import AdminMeterIndicatorForm


class AdminMeterIndicatorsCreateView(
    SuccessUrlMixin,
    SuccessMessageMixin,
    MeterIndicatorPermissionRequiredMixin,
    HouseUserRequiredMixin,
    CreateView
):
    template_name = 'meter_indicators/adminlte/create.html'
    success_message = 'Новий показник рахунку успішно створено'
    form_class = AdminMeterIndicatorForm

    def get_form(self, **kwargs):
        flat_id = self.request.GET.get('flat_id', None)
        service_id = self.request.GET.get('service_id', None)

        initial = {}

        if flat_id:
            flat = Flat.objects.select_related('house', 'section').get(pk=flat_id)

            initial['house'] = flat.house
            initial['section'] = flat.section
            initial['flat'] = flat

            if service_id:
                service = Service.objects.get(pk=service_id)

                initial['service'] = service

            return AdminMeterIndicatorForm(
                self.request.POST or None,
                initial=initial
            )

        return AdminMeterIndicatorForm(self.request.POST or None)
