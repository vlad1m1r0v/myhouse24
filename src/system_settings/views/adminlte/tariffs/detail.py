from django.views.generic import DetailView

from src.system_settings.models import Tariff
from .mixin import TariffPermissionRequiredMixin


class AdminTariffDetailView(TariffPermissionRequiredMixin,
                            DetailView):
    template_name = 'system_settings/adminlte/tariffs/detail.html'
    model = Tariff
    context_object_name = 'tariff'