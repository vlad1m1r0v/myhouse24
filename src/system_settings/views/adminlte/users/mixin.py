from src.core.utils import CustomPermissionRequiredMixin


class UserPermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.users'
    permission_denied_message = 'У Вас немає доступу до користувачів'