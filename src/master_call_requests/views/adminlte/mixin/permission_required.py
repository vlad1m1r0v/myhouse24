from src.core.utils import CustomPermissionRequiredMixin


class MasterCallRequestPermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.master_call_requests'
    permission_denied_message = 'У Вас немає доступу до заявок виклику майстра'