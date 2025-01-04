from ajax_datatable import AjaxDatatableView
from django.urls import reverse

from src.system_settings.models import Tariff


class AdminTariffsDatatableView(AjaxDatatableView):
    model = Tariff
    title = 'Тарифи'
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'Всі']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'name', 'title': 'Назва', 'visible': True, 'searchable': False},
        {'name': 'description', 'title': 'Опис', 'visible': True, 'searchable': False, },
        {'name': 'updated_at', 'title': 'Дата редагування', 'visible': True, 'searchable': False, },
        {'name': 'button_group', 'title': '', 'placeholder': True, 'visible': True, 'searchable': False,
         'orderable': False, },
    ]

    def customize_row(self, row, obj):
        row['button_group'] = \
            f"""
            <div class="btn-group pull-right">
                <a href={reverse('adminlte:system-settings:tariffs:create')}?tariff_id={obj.id} class="btn btn-default btn-sm" title='Копіювати'>
                    <i class="fa fa-clone"></i>
                </a>
                 <a href={reverse('adminlte:system-settings:tariffs:update', kwargs={'pk': obj.id})} class="btn btn-default btn-sm" title="Редагувати">
                    <i class="fa fa-pencil"></i>
                </a>
                <button data-href={reverse('adminlte:system-settings:tariffs:delete', kwargs={'pk': obj.id})} class="btn btn-default btn-sm delete-button">
                    <i class="fa fa-trash" title="Видалити"></i>
                </button>
            </div>
            """

        row['updated_at'] = str(obj.updated_at.strftime("%d.%m.%Y-%-H:%M"))