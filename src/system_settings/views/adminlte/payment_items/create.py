from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from src.system_settings.forms import AdminPaymentItemForm
from src.system_settings.models import PaymentItem
from .mixin import PaymentItemPermissionRequiredMixin


class AdminPaymentItemCreateView(SuccessMessageMixin,
                                 PaymentItemPermissionRequiredMixin,
                                 CreateView):
    model = PaymentItem
    template_name = 'adminlte/system_settings/payment_items/create.html'
    form_class = AdminPaymentItemForm
    success_url = reverse_lazy('adminlte:system-settings:payment-items:list')
    success_message = 'Статтю платежу успішно створено'
