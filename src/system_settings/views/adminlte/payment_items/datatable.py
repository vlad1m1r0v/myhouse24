from ajax_datatable import AjaxDatatableView
from django.urls import reverse
from src.system_settings.models import PaymentItem


class AdminPaymentItemsDatatableView(AjaxDatatableView):
    model = PaymentItem
    title = 'Статті платежів'
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'Всі']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'name', 'title': 'Назва', 'visible': True, },
        {'name': 'type', 'title': 'Прихід / Витрата', 'visible': True, },
        {'name': 'button_group',
         'title': '',
         'placeholder': True, 'visible': True,
         'searchable': False,
         'orderable': False, },
    ]

    def customize_row(self, row, obj):
        if obj.type == 'income':
            row['type'] = f"<p class='text-green'>{obj.get_type_display()}</p>"
        else:
            row['type'] = f"<p class='text-red'>{obj.get_type_display()}</p>"

        row['button_group'] = \
            f"""
            <div class="btn-group pull-right">
                <a class="btn btn-default btn-sm" href={reverse('adminlte:system-settings:payment-items:update', kwargs={'pk': obj.id})} title="Редагувати">
                    <i class="fa fa-pencil"></i>
                </a> 
                <button class="btn btn-default btn-sm delete-button" data-href={reverse('adminlte:system-settings:payment-items:delete', kwargs={'pk': obj.id})} title="Видалити">
                    <i class="fa fa-trash"></i>
                </button>
            </div>
            """
