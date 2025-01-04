from django.views.generic import TemplateView

from .mixin import TariffPermissionRequiredMixin


class AdminTariffsView(TariffPermissionRequiredMixin,
                       TemplateView):
    template_name = 'adminlte/system_settings/tariffs/list.html'