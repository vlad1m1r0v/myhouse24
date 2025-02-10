from src.core.utils import CustomPermissionRequiredMixin


class PersonalAccountPermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.personal_accounts'
    permission_denied_message = 'У Вас немає доступу до особових рахунків'