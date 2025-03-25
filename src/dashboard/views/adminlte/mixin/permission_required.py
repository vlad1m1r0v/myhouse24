from src.core.utils import CustomPermissionRequiredMixin


class StatisticsPermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.statistics'
    permission_denied_message = 'У Вас немає доступу до статистики'