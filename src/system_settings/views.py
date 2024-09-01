from ajax_datatable import AjaxDatatableView
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from src.system_settings.models import PaymentItem


class AdminPaymentItemsView(PermissionRequiredMixin, TemplateView, ):
    template_name = 'system_settings/payment_items/list_payments_items.html'
    permission_required = ('authentication.payment_items',)

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до статей платежів')
        return redirect(reverse('authentication_adminlte_login'))


class AdminPaymentItemsDatatableView(AjaxDatatableView):
    model = PaymentItem
    title = 'Payment Items'
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'Всі']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'name', 'title': 'Назва', 'visible': True, },
        {'name': 'type', 'title': 'Прихід / Витрата', 'visible': True, },
    ]

    def customize_row(self, row, obj):
        if obj.type == 'income':
            row['type'] = f"<p class='text-green'>{obj.get_type_display()}</p>"
        else:
            row['type'] = f"<p class='text-red'>{obj.get_type_display()}</p>"
        return
