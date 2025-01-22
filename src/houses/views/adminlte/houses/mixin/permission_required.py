from src.core.utils import CustomPermissionRequiredMixin


class HousePermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.houses'
    permission_denied_message = 'У Вас немає доступу до будинків'