from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from src.system_settings.forms import AdminPaymentItemForm
from src.system_settings.models import PaymentItem
from .mixin import PaymentItemPermissionRequiredMixin

class AdminPaymentItemUpdateView(SuccessMessageMixin,
                                 PaymentItemPermissionRequiredMixin,
                                 UpdateView):
    model = PaymentItem
    template_name = 'system_settings/adminlte/payment_items/update.html'
    form_class = AdminPaymentItemForm
    success_url = reverse_lazy('adminlte:system-settings:payment-items:list')
    success_message = 'Статтю платежу успішно оновлено'
