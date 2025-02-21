from ajax_datatable import AjaxDatatableView
from django.template.loader import render_to_string

from src.system_settings.models import PaymentItem


class AdminPaymentItemsDatatableView(AjaxDatatableView):
    model = PaymentItem

    column_defs = [
        {'name': 'pk'},
        {'name': 'name'},
        {'name': 'type'},
        {'name': 'actions'},
    ]

    def get_initial_queryset(self, request=None):
        return self.model.objects.order_by('id')

    def customize_row(self, row, obj):
        row['name'] = obj.name

        row['type'] = render_to_string(
            template_name='system_settings/adminlte/payment_items/_partials/type.html',
            context={'object': obj}
        )

        row['actions'] = render_to_string(
            template_name='system_settings/adminlte/payment_items/_partials/actions.html',
            context={'object': obj}
        )