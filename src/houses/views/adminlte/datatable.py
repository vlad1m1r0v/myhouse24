from ajax_datatable import AjaxDatatableView
from django.urls import reverse

from src.houses.models import House


class AdminHousesDatatableView(AjaxDatatableView):
    model = House
    title = 'Домівки'
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'Всі']]
    search_values_separator = '+'

    column_defs = [
        {
            'name': 'id',
            'title': '#',
            'visible': True,
        },
        {
            'name': 'name',
            'title': 'Назва',
            'visible': True,
        },
        {
            'name': 'address',
            'title': 'Адреса',
            'visible': True
        },
        {
            'name': 'button_group',
            'title': '',
            'placeholder': True,
            'visible': True,
            'searchable': False,
            'orderable': False,
        },
    ]

    def customize_row(self, row, obj):
        row['button_group'] = \
            f"""
            <div class="btn-group pull-right">
                 <a href={reverse('adminlte:houses:update', kwargs={'pk': obj.id})} class="btn btn-default btn-sm" title="Редагувати">
                    <i class="fa fa-pencil"></i>
                </a>
                <button data-href={reverse('adminlte:houses:delete', kwargs={'pk': obj.id})} class="btn btn-default btn-sm delete-button" title="Видалити">
                    <i class="fa fa-trash"></i>
                </button>
            </div>
            """

    def get_initial_queryset(self, request=None):
        user = request.user
        if user.is_superuser:
            return super().get_initial_queryset(request)
        return super().get_initial_queryset(request).filter(users__user=user)
