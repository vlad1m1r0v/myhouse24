from django.db.models import Prefetch
from django.views.generic import TemplateView

from src.core.utils.permissions import OwnerRequiredMixin
from src.flats.models import Flat
from src.system_settings.models import Tariff, TariffService


class AccountTariffDetailView(
    OwnerRequiredMixin,
    TemplateView
):
    template_name = 'system_settings/account/tariff.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        flat_id = self.request.GET.get('flat_id')
        flat = Flat.objects.select_related('house').get(id=flat_id)
        tariff = (Tariff.objects
                  .prefetch_related(Prefetch('services', queryset=TariffService.objects
                                             .select_related('service', 'service__unit')))
                  .get(pk=flat.tariff_id))

        context['flat'] = flat
        context['tariff'] = tariff

        return context
