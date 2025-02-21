from ajax_datatable import AjaxDatatableView
from django.db.models import Q
from django.template.loader import render_to_string

from src.houses.models import House


class AdminHousesDatatableView(AjaxDatatableView):
    model = House

    disable_queryset_optimization = True
    disable_queryset_optimization_only = True
    disable_queryset_optimization_select_related = True
    disable_queryset_optimization_prefetch_related = True

    column_defs = [
        {'name': 'pk'},
        {'name': 'name'},
        {'name': 'address'},
        {'name': 'actions'}
    ]

    def get_initial_queryset(self, request=None):
        user = request.user
        if user.is_superuser:
            return super().get_initial_queryset(request)
        return super().get_initial_queryset(request).filter(users__user=user)

    def filter_queryset(self, params, qs):
        name = self.request.GET.get('name')
        address = self.request.GET.get('address')

        filters = Q()

        if name:
            filters &= Q(name__icontains=name)

        if address:
            filters &= Q(address__icontains=address)

        qs = qs.filter(filters)
        return qs

    def customize_row(self, row, obj):
        row['pk'] = obj.pk

        row['name'] = obj.name

        row['address'] = obj.address

        row['actions'] = render_to_string(
            template_name='houses/adminlte/_partials/actions.html',
            context={'object': obj}
        )
