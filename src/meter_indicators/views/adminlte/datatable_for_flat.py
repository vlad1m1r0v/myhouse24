from datetime import datetime

from ajax_datatable import AjaxDatatableView
from django.db.models import Q
from django.template.defaultfilters import date as _date
from django.template.loader import render_to_string

from src.meter_indicators.models import MeterIndicator


class AdminMeterIndicatorsDatatableForFlatView(AjaxDatatableView):
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
        {'name': 'actions'}
    ]

    def get_initial_queryset(self, request=None):
        qs = (self.model.objects
              .select_related('house', 'section', 'flat', 'service', 'service__unit'))

        return qs

    def filter_queryset(self, params, qs):
        # retrieved in template through new UrlSearchParams()
        # flat_id is required
        flat_id = self.request.GET.get('flat_id')
        # service_id is optional
        service_id = self.request.GET.get('service_id')
        # retrieved through filtering inputs and selects
        # all fields optional
        no = self.request.GET.get('no')
        status = self.request.GET.get('status')
        date = self.request.GET.get('date')

        filters = Q()

        if flat_id:
            filters &= Q(flat_id=flat_id)

        if service_id:
            filters &= Q(service_id=service_id)

        if no:
            filters &= Q(no__icontains=no)

        if status:
            filters &= Q(status=status)

        if date:
            start = datetime.strptime(date.split(' - ')[0], '%d.%m.%Y')
            end = datetime.strptime(date.split(' - ')[1], '%d.%m.%Y')
            filters &= Q(date__gte=start)
            filters &= Q(date__lte=end)

        qs = qs.filter(filters)
        return qs

    def sort_queryset(self, params, qs):
        for order in params['orders']:
            field = order.column_link.get_field_search_path()

            if field == 'date' or field == 'month':
                if order.ascending:
                    return qs.order_by('date')
                return qs.order_by('-date')

            break

        return super().sort_queryset(params, qs)

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

        row['actions'] = render_to_string(
            template_name='meter_indicators/adminlte/_partials/actions.html',
            context={'object': obj}
        )
