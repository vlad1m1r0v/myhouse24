from django.contrib import messages
from django.shortcuts import redirect
from django.views import View

from ...models import ReadMessage
from src.core.utils.permissions import OwnerRequiredMixin


class AccountMessagesDeleteView(
    OwnerRequiredMixin,
    View
):
    def post(self, request, pk):
        read_message = ReadMessage(user_id=request.user.id, message_id=pk)
        read_message.save()

        messages.success(request, 'Повідомлення позначено як прочитане')
        return redirect('account:messages:list')