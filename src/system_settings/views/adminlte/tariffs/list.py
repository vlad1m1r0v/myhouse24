from django.views.generic import TemplateView

from .mixin import TariffPermissionRequiredMixin


class AdminTariffsView(TariffPermissionRequiredMixin,
                       TemplateView):
    template_name = 'system_settings/adminlte/tariffs/list.html'