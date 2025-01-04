from django.views.generic import TemplateView

from .mixin import PaymentItemPermissionRequiredMixin


class AdminPaymentItemsView(PaymentItemPermissionRequiredMixin,
                            TemplateView):
    template_name = 'adminlte/system_settings/payment_items/list.html'