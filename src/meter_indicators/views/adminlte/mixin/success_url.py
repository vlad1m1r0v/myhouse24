from typing import TypeVar, Protocol, cast

from django.forms import BaseForm
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.db.models import Q
from src.flats.models import Flat
from src.meter_indicators.forms import AdminMeterIndicatorForm
from src.system_settings.models import Service

FormT = TypeVar("FormT", bound=BaseForm)


class SuccessUrlMixinProtocol(Protocol[FormT]):
    request: HttpRequest

    def get_form(self, form_class: type[FormT] | None = None) -> FormT: ...


class SuccessUrlMixin:
    def get_success_url(self: SuccessUrlMixinProtocol[AdminMeterIndicatorForm]) -> str:
        if 'save_and_add_new' in self.request.POST:
            form = self.get_form()

            if form.is_valid():

                flat: Flat | None = form.cleaned_data.get('flat')
                service: Service | None = form.cleaned_data.get('service')

                if flat and service:
                    sorted_flats = Flat.objects.order_by('house', 'section', 'no')
                    try:
                        next_flat = sorted_flats.filter(
                            Q(house__gt=flat.house) |
                            Q(house=flat.house, section__gt=flat.section) |
                            Q(house=flat.house, section=flat.section, no__gt=flat.no)
                        ).first()

                        if next_flat:
                            return (
                                f"{reverse_lazy('adminlte:meter-indicators:create')}"
                                f"?flat_id={next_flat.id}&service_id={service.id}"
                            )
                    except Flat.DoesNotExist:
                        pass

                return reverse_lazy('adminlte:meter-indicators:create')

        return reverse_lazy('adminlte:meter-indicators:list')
