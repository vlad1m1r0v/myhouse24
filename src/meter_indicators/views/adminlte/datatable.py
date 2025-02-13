from ajax_datatable import AjaxDatatableView
from django.db.models import Q
from django.template.loader import render_to_string

from src.meter_indicators.models import MeterIndicator


class AdminMeterIndicatorsDatatableView(AjaxDatatableView):
    model = MeterIndicator

    disable_queryset_optimization = True
    disable_queryset_optimization_only = True
    disable_queryset_optimization_select_related = True
    disable_queryset_optimization_prefetch_related = True

    column_defs = [
        {'name': 'pk'},
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
              .select_related('house', 'section', 'flat', 'service', 'service__unit')
              .prefetch_related('house__users__user'))

        if not request.user.is_superuser:
            qs = qs.filter(house__users__user=request.user)

        return qs

    def filter_queryset(self, params, qs):
        house = self.request.GET.get('house')
        section = self.request.GET.get('section')
        flat = self.request.GET.get('flat')
        service = self.request.GET.get('service')

        filters = Q()

        if house:
            filters &= Q(house_id=house)

        if section:
            filters &= Q(section_id=section)

        if flat:
            filters &= Q(flat_id=flat)

        if service:
            filters &= Q(service_id=service)

        qs = qs.filter(filters)
        return qs

    def sort_queryset(self, params, qs):
        for order in params['orders']:
            field = order.column_link.get_field_search_path()

            if field == 'flat':
                if order.ascending:
                    return qs.order_by('flat__no')
                return qs.order_by('-flat__no')

            break

        return super().sort_queryset(params, qs)

    def customize_row(self, row, obj):
        row['house'] = obj.house.name

        row['section'] = obj.section.name

        row['flat'] = f"{obj.flat.no}, {obj.house.name}"

        row['service'] = obj.service.name

        row['unit'] = obj.service.unit.unit

        row['actions'] = render_to_string(
            template_name='meter_indicators/adminlte/_partials/actions.html',
            context={'object': obj}
        )
