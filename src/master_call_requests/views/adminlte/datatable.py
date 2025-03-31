from datetime import datetime

from ajax_datatable import AjaxDatatableView
from django.db.models import Q, ExpressionWrapper, F
from django.db.models.fields import DateTimeField
from django.template.loader import render_to_string

from src.master_call_requests.models import MasterCallRequest


class AdminMasterCallRequestsDatatableView(AjaxDatatableView):
    model = MasterCallRequest

    disable_queryset_optimization = True
    disable_queryset_optimization_only = True
    disable_queryset_optimization_select_related = True
    disable_queryset_optimization_prefetch_related = True

    column_defs = [
        {'name': 'no'},
        {'name': 'datetime'},
        {'name': 'master_type'},
        {'name': 'description'},
        {'name': 'flat'},
        {'name': 'owner'},
        {'name': 'phone'},
        {'name': 'master'},
        {'name': 'status'},
        {'name': 'actions'}
    ]

    def get_initial_queryset(self, request=None):
        qs = (self.model.objects.
              select_related('flat', 'flat__house', 'flat_owner', 'master', 'master_type').
              prefetch_related('flat__house__users__user').
              annotate(datetime=ExpressionWrapper(F('date') + F('time'), output_field=DateTimeField())))

        if not request.user.is_superuser:
            qs = qs.filter(flat__house__users__user=request.user)

        return qs

    def filter_queryset(self, params, qs):
        no = self.request.GET.get('no')
        date = self.request.GET.get('date')
        master_type = self.request.GET.get('master_type')
        description = self.request.GET.get('description')
        flat = self.request.GET.get('flat')
        owner = self.request.GET.get('owner')
        phone = self.request.GET.get('phone')
        master = self.request.GET.get('master')
        status = self.request.GET.get('status')

        filters = Q()

        if no:
            filters &= Q(pk=no)

        if date:
            start = datetime.strptime(date.split(' - ')[0], '%d.%m.%Y')
            filters &= Q(date__gte=start)

            end = datetime.strptime(date.split(' - ')[1], '%d.%m.%Y')
            filters &= Q(date__lte=end)

        if master_type:
            filters &= Q(master_type=master_type)

        if description:
            filters &= Q(description__icontains=description)

        if flat:
            filters &= Q(flat__no__icontains=flat)

        if owner:
            filters &= Q(flat_owner=owner)

        if phone:
            filters &= Q(flat_owner__phone_number__icontains=phone)

        if master:
            filters &= Q(master=master)

        if status:
            filters &= Q(status=status)

        return qs.filter(filters)

    def sort_queryset(self, params, qs):
        for order in params['orders']:
            field = order.column_link.get_field_search_path()

            if field == 'no':
                if order.ascending:
                    return qs.order_by('pk')
                return qs.order_by('-pk')

            if field == 'flat':
                if order.ascending:
                    return qs.order_by('flat__no')
                return qs.order_by('-flat__no')

            if field == 'date':
                if order.ascending:
                    return qs.order_by('datetime')
                return qs.order_by('-datetime')

            break

        return super().sort_queryset(params, qs)

    def customize_row(self, row, obj):
        row['no'] = obj.pk

        row['datetime'] = obj.datetime.strftime("%d.%m.%Y - %H:%M")

        row['master_type'] = str(obj.master_type) if obj.master_type else '(Не вибрано)'

        row['description'] = obj.description

        row['flat'] = f"кв.{obj.flat.no}, {obj.flat.house.name}"

        row['owner'] = str(obj.flat_owner)

        row['phone'] = obj.flat_owner.phone_number if obj.flat_owner.phone_number else '(Не вказано)'

        row['master'] = str(obj.master) if obj.master else '(Не вибрано)'

        row['status'] = render_to_string(
            template_name='master_call_requests/adminlte/_partials/status_label.html',
            context={'object': obj}
        )

        row['actions'] = render_to_string(
            template_name='master_call_requests/adminlte/_partials/actions.html',
            context={'object': obj}
        )
