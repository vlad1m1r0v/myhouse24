from src.core.utils import CustomPermissionRequiredMixin


class WebsitePermissionRequiredMixin(CustomPermissionRequiredMixin):
    permission_required = 'authentication.website_management'
    permission_denied_message = 'У Вас немає доступу до управління сайтом'