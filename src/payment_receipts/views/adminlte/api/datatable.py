from datetime import datetime

from ajax_datatable import AjaxDatatableView
from django.db.models import Q
from django.template.defaultfilters import date as _date
from django.template.loader import render_to_string

from src.meter_indicators.models import MeterIndicator


class AdminReceiptsIndicatorsDatatableView(AjaxDatatableView):
    model = MeterIndicator

    disable_queryset_optimization = True
    disable_queryset_optimization_only = True
    disable_queryset_optimization_select_related = True
    disable_queryset_optimization_prefetch_related = True

    column_defs = [
        {'name': 'pk'},
        {'name': 'no'},
        {'name': 'status'},
        {'name': 'date'},
        {'name': 'month'},
        {'name': 'house'},
        {'name': 'section'},
        {'name': 'flat'},
        {'name': 'service'},
        {'name': 'value'},
        {'name': 'unit'},
    ]

    def get_initial_queryset(self, request=None):
        qs = (self.model.objects
              .select_related('house', 'section', 'flat', 'service', 'service__unit'))

        return qs

    def filter_queryset(self, params, qs):
        house_id = self.request.GET.get('house_id')
        section_id = self.request.GET.get('section_id')
        flat_id = self.request.GET.get('flat_id')

        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        filters = Q()

        if house_id:
            filters &= Q(house_id=house_id)

        if section_id:
            filters &= Q(section_id=section_id)

        if flat_id:
            filters &= Q(flat_id=flat_id)

        if date_from:
            date_from_parsed = datetime.strptime(date_from, '%d.%m.%Y').date()
            filters &= Q(date__gte=date_from_parsed)

        if date_to:
            date_to_parsed = datetime.strptime(date_to, '%d.%m.%Y').date()
            filters &= Q(date__lte=date_to_parsed)

        qs = qs.filter(filters)
        return qs

    def customize_row(self, row, obj):
        row['no'] = obj.no

        row['status'] = render_to_string(
            template_name='meter_indicators/adminlte/_partials/status_label.html',
            context={'object': obj}
        )

        date = datetime.strptime(str(obj.date), "%Y-%m-%d")
        row['date'] = date.strftime("%d.%m.%Y")

        row['month'] = _date(obj.date, "F")

        row['house'] = obj.house.name

        row['section'] = obj.section.name

        row['flat'] = obj.flat.no

        row['service'] = obj.service.name

        row['value'] = obj.value

        row['unit'] = obj.service.unit.unit