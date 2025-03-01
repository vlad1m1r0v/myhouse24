from datetime import datetime
from django.db.models import Q, Subquery, OuterRef, FloatField
from django.http import JsonResponse
from django.views import View

from src.meter_indicators.models import MeterIndicator
from src.system_settings.models import TariffService


class AdminReceiptsIndicatorsView(View):
    def get(self, *args, **kwargs):
        flat_id = self.request.GET.get('flat_id')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if not flat_id:
            return JsonResponse([], safe=False)

        filters = Q(flat_id=flat_id, status='new')

        if date_from:
            date_from_parsed = datetime.strptime(date_from, '%d.%m.%Y').date()
            filters &= Q(date__gte=date_from_parsed)

        if date_to:
            date_to_parsed = datetime.strptime(date_to, '%d.%m.%Y').date()
            filters &= Q(date__lte=date_to_parsed)

        price_subquery = Subquery(
            TariffService.objects.filter(
                tariff=OuterRef('flat__tariff'),
                service=OuterRef('service')
            ).values('price')[:1],
            output_field=FloatField()
        )

        indicators = (
            MeterIndicator.objects
            .select_related('flat', 'flat__tariff')
            .filter(filters)
            .annotate(price=price_subquery)
            .order_by('service_id')
            .values('id', 'service_id', 'value', 'price')
        )

        return JsonResponse(list(indicators), safe=False)