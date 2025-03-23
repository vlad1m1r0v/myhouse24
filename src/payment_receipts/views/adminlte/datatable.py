from datetime import datetime

from ajax_datatable import AjaxDatatableView
from django.db.models import OuterRef, Exists, Q
from django.template.loader import render_to_string
from django.utils.formats import date_format

from src.houses.models import HouseUser
from src.payment_receipts.models import Receipt


class AdminReceiptsDatatableView(AjaxDatatableView):
    model = Receipt

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
        {'name': 'flat'},
        {'name': 'owner'},
        {'name': 'is_complete'},
        {'name': 'total_price'},
        {'name': 'actions'}
    ]

    def get_initial_queryset(self, request=None):
        subquery = HouseUser.objects.filter(
            house=OuterRef("flat__house"),
            user=self.request.user
        ).values("id")

        qs = (self.model.objects
              .select_related('flat', 'flat__house', 'flat__owner')
              .with_total_price())

        if not self.request.user.is_superuser:
            qs = (qs.prefetch_related('flat__house__users')
                  .annotate(user_has_access=Exists(subquery))
                  .filter(user_has_access=True))

        return qs

    def filter_queryset(self, params, qs):
        no = self.request.GET.get("no")
        status = self.request.GET.get("status")
        date = self.request.GET.get('date')
        month = self.request.GET.get('month')
        flat = self.request.GET.get('flat')
        owner = self.request.GET.get('owner')
        is_complete = self.request.GET.get('is_complete')

        filters = Q()

        if no:
            filters &= Q(no__icontains=no)

        if status:
            filters &= Q(status=status)

        if date:
            start = datetime.strptime(date.split(' - ')[0], '%d.%m.%Y')
            filters &= Q(period_from__gte=start)

            end = datetime.strptime(date.split(' - ')[1], '%d.%m.%Y')
            filters &= Q(period_to__lte=end)

        if month:
            month, year = map(int, month.split('.'))

            filters &= Q(
                period_to__year=year,
                period_to__month=month
            )

        if flat:
            filters &= Q(flat__no__icontains=flat)

        if owner:
            filters &= Q(flat__owner=owner)

        if is_complete:
            filters &= Q(is_complete=True if is_complete == 'true' else False)

        return qs.filter(filters)

    def sort_queryset(self, params, qs):
        for order in params['orders']:
            field = order.column_link.get_field_search_path()

            if field == 'date':
                if order.ascending:
                    return qs.order_by('date')
                return qs.order_by('-date')

            if field == 'month':
                if order.ascending:
                    return qs.order_by('period_to')
                return qs.order_by('-period_to')

        qs = qs.order_by('-id')
        return qs

    def customize_row(self, row, obj):
        row['pk'] = int(obj.pk)

        row['no'] = obj.no

        row['status'] = render_to_string(
            template_name='payment_receipts/adminlte/_partials/status.html',
            context={'object': obj}
        )

        row['date'] = obj.date.strftime('%d.%m.%Y')

        row['month'] = date_format(obj.period_to, 'F Y')

        row['flat'] = f"{obj.flat.no}, {obj.flat.house.name}"

        row['owner'] = (f"{obj.flat.owner.last_name} "
                        f"{obj.flat.owner.first_name} "
                        f"{obj.flat.owner.middle_name}") if obj.flat.owner else '(Не вказано)'

        row['is_complete'] = 'Проведена' if obj.is_complete else 'Не проведена'

        row['total_price'] = obj.total_price

        row['actions'] = render_to_string(
            template_name='payment_receipts/adminlte/_partials/actions.html',
            context={'object': obj}
        )
