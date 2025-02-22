from src.core.utils import CustomPermissionRequiredMixin


class MasterCallRequestPermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.service_call_requests'
    permission_denied_message = 'У Вас немає доступу до заявок виклику майстра'