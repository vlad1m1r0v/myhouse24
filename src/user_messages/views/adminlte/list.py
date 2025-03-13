from django.views.generic import TemplateView
from .mixin import MessagePermissionRequiredMixin

class AdminMessagesListView(
    MessagePermissionRequiredMixin,
    TemplateView
):
    template_name = 'user_messages/adminlte/list.html'