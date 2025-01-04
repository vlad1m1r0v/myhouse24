from src.core.utils import CustomPermissionRequiredMixin


class TariffPermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.tariffs'
    permission_denied_message = 'У Вас немає доступу до тарифів'

