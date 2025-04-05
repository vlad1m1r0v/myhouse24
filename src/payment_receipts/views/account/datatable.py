from datetime import datetime

from ajax_datatable import AjaxDatatableView
from django.db.models import Q
from django.template.loader import render_to_string

from src.payment_receipts.models import Receipt


class AccountReceiptsDatatableView(AjaxDatatableView):
    model = Receipt

    disable_queryset_optimization = True
    disable_queryset_optimization_only = True
    disable_queryset_optimization_select_related = True
    disable_queryset_optimization_prefetch_related = True

    column_defs = [
        {'name': 'pk'},
        {'name': 'no'},
        {'name': 'date'},
        {'name': 'status'},
        {'name': 'total_price'}
    ]

    def get_initial_queryset(self, request=None):
        return self.model.objects.with_total_price()

    def filter_queryset(self, params, qs):
        flat = self.request.GET.get('flat')
        date = self.request.GET.get('date')
        status = self.request.GET.get("status")

        filters = Q()

        if flat:
            filters &= Q(flat=flat)

        if status:
            filters &= Q(status=status)

        if date:
            date = datetime.strptime(date, '%d.%m.%Y')
            filters &= Q(date=date)

        return qs.filter(filters)

    def sort_queryset(self, params, qs):
        for order in params['orders']:
            field = order.column_link.get_field_search_path()

            if field == 'date':
                if order.ascending:
                    return qs.order_by('date')
                return qs.order_by('-date')

        qs = qs.order_by('-id')
        return qs

    def customize_row(self, row, obj):
        row['pk'] = int(obj.pk)

        row['no'] = obj.no

        row['date'] = obj.date.strftime('%d.%m.%Y')

        row['status'] = render_to_string(
            template_name='payment_receipts/shared/_partials/status.html',
            context={'object': obj}
        )

        row['total_price'] = obj.total_price
