from django.views.generic import TemplateView

from .mixin import PaymentItemPermissionRequiredMixin


class AdminPaymentItemsView(PaymentItemPermissionRequiredMixin,
                            TemplateView):
    template_name = 'system_settings/adminlte/payment_items/list.html'