from src.core.utils import CustomPermissionRequiredMixin


class ReceiptsPermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.receipts'
    permission_denied_message = 'У Вас немає доступу до квитанцій'