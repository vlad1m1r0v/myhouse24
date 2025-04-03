from django.views.generic import DetailView

from src.user_messages.models import Message


class AccountMessageDetailView(DetailView):
    model = Message
    context_object_name = 'message'
    template_name = 'user_messages/account/detail.html'

    def get_queryset(self):
        return super().get_queryset().select_related('creator')