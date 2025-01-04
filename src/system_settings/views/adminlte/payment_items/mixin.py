from src.core.utils import CustomPermissionRequiredMixin


class PaymentItemPermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.payment_items'
    permission_denied_message = 'У Вас немає доступу до статей платежів'