from datetime import datetime
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.views import View

from src.meter_indicators.models import MeterIndicator


class AdminReceiptsIndicatorsView(View):
    def get(self, *args, **kwargs):
        flat_id = self.request.GET.get('flat_id')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if not flat_id:
            return JsonResponse({'error': 'flat_id є обов’язковим параметром'}, status=400)

        filters = Q(flat_id=flat_id)

        if date_from:
            date_from_parsed = datetime.strptime(date_from, '%d.%m.%Y').date()
            filters &= Q(date__gte=date_from_parsed)

        if date_to:
            date_to_parsed = datetime.strptime(date_to, '%d.%m.%Y').date()
            filters &= Q(date__lte=date_to_parsed)

        indicators = (
            MeterIndicator.objects
            .filter(filters)
            .values('id', 'service_id')
            .annotate(value=Sum('value'))
        )

        return JsonResponse(list(indicators), safe=False)
