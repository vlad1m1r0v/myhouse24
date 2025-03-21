from ajax_datatable import AjaxDatatableView
from django.db.models import Q
from django.template.loader import render_to_string

from src.flats.models import Flat


class AdminFlatsDatatableView(AjaxDatatableView):
    model = Flat

    disable_queryset_optimization = True
    disable_queryset_optimization_only = True
    disable_queryset_optimization_select_related = True
    disable_queryset_optimization_prefetch_related = True

    column_defs = [
        {'name': 'pk'},
        {'name': 'flat'},
        {'name': 'house'},
        {'name': 'section'},
        {'name': 'floor'},
        {'name': 'owner'},
        {'name': 'balance'},
        {'name': 'actions'}
    ]

    def get_initial_queryset(self, request=None):
        qs = (self.model.objects
            .with_debt()
            .with_balance()
            .with_related()
        )

        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(house__users__user__in=[self.request.user])

    def sort_queryset(self, params, qs):
        for order in params['orders']:
            field = order.column_link.get_field_search_path()

            if field == 'flat':
                if order.ascending:
                    return qs.order_by('no')
                return qs.order_by('-no')

            if field == 'house':
                if order.ascending:
                    return qs.order_by('house__pk')
                return qs.order_by('-house__pk')

            if field == 'section':
                if order.ascending:
                    return qs.order_by('section__pk')
                return qs.order_by('-section__pk')

            if field == 'floor':
                if order.ascending:
                    return qs.order_by('floor__pk')
                return qs.order_by('-floor__pk')

            if field == 'owner':
                if order.ascending:
                    return qs.order_by('owner__pk')
                qs.order_by('-owner__pk')

        qs = qs.order_by('-id')
        return qs

    def filter_queryset(self, params, qs):
        flat = self.request.GET.get('flat')
        house = self.request.GET.get('house')
        section = self.request.GET.get('section')
        floor = self.request.GET.get('floor')
        owner = self.request.GET.get('owner')
        has_debt = self.request.GET.get('has_debt')

        filters = Q()

        if flat:
            filters &= Q(no__icontains=flat)

        if house:
            filters &= Q(house__pk=house)

        if section:
            filters &= Q(section__pk=section)

        if floor:
            filters &= Q(floor__pk=floor)

        if owner:
            filters &= Q(owner__pk=owner)

        if has_debt:
            filters &= Q(has_debt=True if has_debt == 'true' else False)

        return qs.filter(filters)

    def customize_row(self, row, obj):
        row['pk'] = int(obj.pk)

        row['flat'] = obj.no

        row['house'] = obj.house.name if obj.house else '(Не вказано)'

        row['section'] = obj.section.name if obj.section else '(Не вказано)'

        row['floor'] = obj.floor.name if obj.floor else '(Не вказано)'

        row['owner'] = f"{obj.owner.last_name} {obj.owner.first_name} {obj.owner.middle_name}" if obj.owner else '(Не вказано)'

        row['balance'] = render_to_string(
            template_name='flats/adminlte/_partials/balance.html',
            context={'object': obj}
        )

        row['actions'] = render_to_string(
            template_name='flats/adminlte/_partials/actions.html',
            context={'object': obj}
        )
