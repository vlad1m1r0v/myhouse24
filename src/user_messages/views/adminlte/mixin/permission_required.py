from src.core.utils import CustomPermissionRequiredMixin


class MessagePermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.messages'
    permission_denied_message = 'У Вас немає доступу до повідомлень'