from ajax_datatable import AjaxDatatableView
from django.template.loader import render_to_string

from src.system_settings.models import Tariff


class AdminTariffsDatatableView(AjaxDatatableView):
    model = Tariff

    column_defs = [
        {'name': 'pk'},
        {'name': 'name'},
        {'name': 'description'},
        {'name': 'updated_at'},
        {'name': 'actions'},
    ]

    def get_initial_queryset(self, request=None):
        return self.model.objects.order_by('id')

    def customize_row(self, row, obj):
        row['name'] = obj.name

        row['description'] = obj.description

        row['updated_at'] = str(obj.updated_at.strftime("%d.%m.%Y-%-H:%M"))

        row['actions'] = render_to_string(
            template_name='system_settings/adminlte/tariffs/_partials/actions.html',
            context={'object': obj}
        )