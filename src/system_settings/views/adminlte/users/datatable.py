from ajax_datatable import AjaxDatatableView
from django.contrib.auth.models import Group
from django.db.models import Value, Subquery, OuterRef, Q
from django.db.models.functions import Concat, Coalesce
from django.urls import reverse

from src.authentication.models import CustomUser, STATUS_CHOICES


class AdminUsersDatatableView(AjaxDatatableView):
    model = CustomUser
    title = 'Користувачі'
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'Всі']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'id', 'title': '#', 'visible': True, },
        {'name': 'full_name', 'title': 'Користувач', 'visible': True, },
        {'name': 'role',
         'title': 'Роль',
         'visible': True,
         'choices': [(group.name, group.name) for group in Group.objects.all()],
         },
        {'name': 'phone_number', 'title': 'Номер телефону', 'visible': True},
        {'name': 'email', 'title': 'Електронна пошта', 'visible': True},
        {'name': 'status',
         'title': 'Статус',
         'visible': True,
         'choices': STATUS_CHOICES,
         },
        {'name': 'button_group',
         'title': '',
         'placeholder': True, 'visible': True,
         'searchable': False,
         'orderable': False,
         },
    ]

    def get_initial_queryset(self, request=None):
        return self.model.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).annotate(
            role=Coalesce(
                Subquery(
                    Group.objects.filter(user=OuterRef('pk')).values('name')[:1]
                ),
                Value(None)
            )
        )

    def customize_row(self, row, obj):
        if obj.status == 'new':
            row['status'] = f"<small class='label label-warning'>{obj.get_status_display()}</small>"
        elif obj.status == 'active':
            row['status'] = f"<small class='label label-success'>{obj.get_status_display()}</small>"
        else:
            row['status'] = f"<small class='label label-danger'>{obj.get_status_display()}</small>"

        row['button_group'] = \
            f"""
            <div class="btn-group pull-right">
                <a class="btn btn-default btn-sm" title='Надіслати запрошення'>
                    <i class="fa fa-repeat"></i>
                </a>
                 <a href={reverse('adminlte:system-settings:users:update', kwargs={'pk': obj.id})} class="btn btn-default btn-sm" title="Редагувати">
                    <i class="fa fa-pencil"></i>
                </a>
                <button {'disabled' if self.request.user.id == obj.id or obj.is_superuser else ''} {'data-href=' + reverse('adminlte:system-settings:users:delete', kwargs={'pk': obj.id}) if self.request.user.id != obj.id else ''} class="btn btn-default btn-sm delete-button"  title="Видалити">
                    <i class="fa fa-trash"></i>
                </button>
            </div>
            """