from src.core.utils import CustomPermissionRequiredMixin


class MeterIndicatorPermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.meter_indicators'
    permission_denied_message = 'У Вас немає доступу до показників рахунків'