from datetime import datetime

from ajax_datatable import AjaxDatatableView
from django.db.models import Q, Value, OuterRef, Exists, Prefetch
from django.db.models.functions import Concat
from django.template.loader import render_to_string

from src.authentication.models import CustomUser
from src.flats.models import Flat
from src.payment_receipts.models import Receipt


class AdminFlatOwnersDatatableView(AjaxDatatableView):
    model = CustomUser

    column_defs = [
        {'name': 'pk'},
        {'name': 'ID'},
        {'name': 'full_name'},
        {'name': 'phone'},
        {'name': 'email'},
        {'name': 'houses'},
        {'name': 'apartments'},
        {'name': 'date'},
        {'name': 'status'},
        {'name': 'has_debt'},
        {'name': 'actions'}
    ]

    def get_initial_queryset(self, request=None):
        owners = (self.model.objects
                  .annotate(has_debt=Exists(
            Receipt.objects.filter(
                flat__owner=OuterRef('pk'),
                status__in=['unpaid', 'partially_paid']
            ).select_related('flat__owner')))
                  .annotate(full_name=Concat('last_name', Value(' '), 'first_name', Value(' '), 'middle_name'))
                  .filter(is_staff=False, is_superuser=False)
                  .prefetch_related(Prefetch('flats', queryset=Flat.objects.select_related('house')))
            .distinct())

        return owners

    def sort_queryset(self, params, qs):
        for order in params['orders']:
            field = order.column_link.get_field_search_path()

            if field == 'full_name':
                if order.ascending:
                    return qs.order_by('full_name')
                return qs.order_by('-full_name')

            if field == 'date':
                if order.ascending:
                    return qs.order_by('date_joined')
                return qs.order_by('-date_joined')

        qs = qs.order_by('-id')
        return qs

    def filter_queryset(self, params, qs):
        ID = self.request.GET.get('ID')
        full_name = self.request.GET.get('full_name')
        phone = self.request.GET.get('phone')
        email = self.request.GET.get('email')
        house = self.request.GET.get('house')
        flat = self.request.GET.get('flat')
        date_joined = self.request.GET.get('date')
        status = self.request.GET.get('status')
        has_debt = self.request.GET.get('has_debt')

        filters = Q()

        if ID:
            filters &= Q(ID__icontains=ID)

        if full_name:
            filters &= Q(full_name__icontains=full_name)

        if phone:
            filters &= Q(phone_number__icontains=phone)

        if email:
            filters &= Q(email__icontains=email)

        if house:
            filters &= Q(flats__house__pk=house)

        if flat:
            filters &= Q(flats__no__in=[int(flat)])

        if date_joined:
            date_obj = datetime.strptime(date_joined, "%d.%m.%Y").date()
            filters &= Q(date_joined__date=date_obj)

        if status:
            filters &= Q(status=status)

        if has_debt:
            filters &= Q(has_debt=True if has_debt == 'true' else False)

        return qs.filter(filters)

    def customize_row(self, row, obj):
        row['pk'] = int(obj.pk)

        row['ID'] = obj.ID

        row['full_name'] = obj.full_name

        row['phone'] = obj.phone_number

        row['email'] = obj.email

        row['houses'] = render_to_string(
            template_name='flat_owners/adminlte/_partials/houses.html',
            context={'object': obj}
        )

        row['apartments'] = render_to_string(
            template_name='flat_owners/adminlte/_partials/flats.html',
            context={'object': obj}
        )

        row['date'] = obj.date_joined.strftime("%d.%m.%Y")

        row['status'] = render_to_string(
            template_name='system_settings/adminlte/users/_partials/status_label.html',
            context={'object': obj}
        )

        row['has_debt'] = 'так' if obj.has_debt else 'ні'

        row['actions'] = render_to_string(
            template_name='flat_owners/adminlte/_partials/actions.html',
            context={'object': obj}
        )
