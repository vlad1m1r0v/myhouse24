from ajax_datatable import AjaxDatatableView
from django.contrib.auth.models import Group
from django.db.models import Q, Value, Subquery, OuterRef, F
from django.db.models.functions import Concat
from django.template.loader import render_to_string

from src.authentication.models import CustomUser


class AdminUsersDatatableView(AjaxDatatableView):
    model = CustomUser

    column_defs = [
        {'name': 'pk'},
        {'name': 'name'},
        {'name': 'role'},
        {'name': 'phone'},
        {'name': 'email'},
        {'name': 'status'},
        {'name': 'actions'}
    ]

    def get_initial_queryset(self, request=None):
        return (self.model.objects.
                filter(Q(is_staff=True) | Q(is_superuser=True)).
                annotate(phone=F('phone_number')).
                annotate(name=Concat('first_name', Value(' '), 'last_name')).
                annotate(role=Subquery(Group.objects.filter(user=OuterRef('pk')).values('name')[:1])).
                order_by('pk'))

    def filter_queryset(self, params, qs):
        name = self.request.GET.get('name')
        role = self.request.GET.get('role')
        phone = self.request.GET.get('phone')
        email = self.request.GET.get('email')
        status = self.request.GET.get('status')

        filters = Q()

        if name:
            filters &= Q(name__icontains=name)

        if role:
            filters &= Q(role=role)

        if phone:
            filters &= Q(phone__icontains=phone)

        if email:
            filters &= Q(email__icontains=email)

        if status:
            filters &= Q(status=status)

        return qs.filter(filters)

    def customize_row(self, row, obj):
        row['pk'] = obj.pk

        row['name'] = obj.name

        row['role'] = obj.role

        row['phone'] = obj.phone

        row['email'] = obj.email

        row['status'] = render_to_string(
            template_name='system_settings/adminlte/users/_partials/status_label.html',
            context={'object': obj}
        )

        row['actions'] = render_to_string(
            template_name='system_settings/adminlte/users/_partials/actions.html',
            context={'object': obj, 'disabled': self.request.user.pk == obj.pk}
        )
