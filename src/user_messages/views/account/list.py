from django.views.generic import TemplateView
from src.core.utils.permissions import OwnerRequiredMixin


class AccountMessagesListView(
    OwnerRequiredMixin,
    TemplateView
):
    template_name = 'user_messages/account/list.html'