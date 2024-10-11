from ajax_datatable import AjaxDatatableView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView

from src.core.utils import is_ajax
from src.system_settings.forms import AdminPaymentItemForm
from src.system_settings.models import PaymentItem


class PaymentItemPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = 'authentication.payment_items'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            if is_ajax(request):
                return JsonResponse(status=403,
                                    data={'success': False, 'message': 'У Вас немає доступу до статей платежів'})
            else:
                messages.error(request, 'У Вас немає доступу до статей платежів')
                logout(request)
                return redirect(reverse('authentication_adminlte_login'))
        return super().dispatch(request, *args, **kwargs)


class AdminPaymentItemsView(PaymentItemPermissionRequiredMixin,
                            TemplateView):
    template_name = 'system_settings/payment_items/list_payments_items.html'


class AdminPaymentItemsDeleteView(PaymentItemPermissionRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        PaymentItem.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})


class AdminPaymentItemCreateView(SuccessMessageMixin,
                                 PaymentItemPermissionRequiredMixin,
                                 CreateView):
    model = PaymentItem
    template_name = 'system_settings/payment_items/create_payment_item.html'
    form_class = AdminPaymentItemForm
    success_url = reverse_lazy('adminlte_payment_items_list')
    success_message = 'Статтю платежу успішно створено'


class AdminPaymentItemUpdateView(SuccessMessageMixin,
                                 PaymentItemPermissionRequiredMixin,
                                 UpdateView):
    model = PaymentItem
    template_name = 'system_settings/payment_items/update_payment_item.html'
    form_class = AdminPaymentItemForm
    success_url = reverse_lazy('adminlte_payment_items_list')
    success_message = 'Статтю платежу успішно оновлено'


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
                <a class="btn btn-default btn-sm" href={reverse('adminlte_payment_items_update', kwargs={'pk': obj.id})} title="Редагувати">
                    <i class="fa fa-pencil"></i>
                </a> 
                <button class="btn btn-default btn-sm delete-button" data-href={reverse('adminlte_payment_items_delete', kwargs={'pk': obj.id})} title="Видалити">
                    <i class="fa fa-trash"></i>
                </button>
            </div>
            """
