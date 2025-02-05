from src.core.utils import CustomPermissionRequiredMixin


class FlatPermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.flats'
    permission_denied_message = 'У Вас немає доступу до квартир'