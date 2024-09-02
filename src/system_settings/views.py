from ajax_datatable import AjaxDatatableView
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView

from src.system_settings.forms import AdminPaymentItemForm
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
        {'name': 'update_or_delete',
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

        row['update_or_delete'] = \
            f"""
        <div class="btn-group pull-right">
            <a class="btn btn-default btn-sm" href={reverse('adminlte_payment_items_update', kwargs={'pk': obj.id})} title="Редагувати">
                <i class="fa fa-pencil"></i>
            </a> 
            <button class="btn btn-default btn-sm delete-button" data-href={reverse('adminlte_payment_items_delete', kwargs={'pk': obj.id})} title="Видалити">
                <i class="fa fa-trash"></i>
            </button>
        </div>
        """


class AdminPaymentItemsDeleteView(View):
    def delete(self, request, *args, **kwargs):
        PaymentItem.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})


class AdminPaymentItemCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
    model = PaymentItem
    template_name = 'system_settings/payment_items/create_payment_item.html'
    form_class = AdminPaymentItemForm
    permission_required = ('authentication.payment_items',)
    success_url = reverse_lazy('adminlte_payment_items_list')
    success_message = 'Статтю платежу успішно створено'

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до статей платежів')
        return redirect(reverse('authentication_adminlte_login'))


class AdminPaymentItemUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    model = PaymentItem
    template_name = 'system_settings/payment_items/create_payment_item.html'
    form_class = AdminPaymentItemForm
    permission_required = ('authentication.payment_items',)
    success_url = reverse_lazy('adminlte_payment_items_list')
    success_message = 'Статтю платежу успішно оновлено'

    def handle_no_permission(self):
        messages.error(self.request, 'У Вас немає доступу до статей платежів')
        return redirect(reverse('authentication_adminlte_login'))
