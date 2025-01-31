from src.core.utils import CustomPermissionRequiredMixin


class FlatOwnerPermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.flat_owners'
    permission_denied_message = 'У Вас немає доступу до власників квартир'