from src.core.utils import CustomPermissionRequiredMixin


class CashBoxPermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.cash_box'
    permission_denied_message = 'У Вас немає доступу до каси'