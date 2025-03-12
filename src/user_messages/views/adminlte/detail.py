from django.views.generic import DetailView

from src.user_messages.models import Message


class AdminMessageDetailView(DetailView):
    model = Message
    context_object_name = 'message'
    template_name = 'user_messages/adminlte/detail.html'

    def get_queryset(self):
        return super().get_queryset().select_related('creator')