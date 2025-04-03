from django.http import JsonResponse
from django.views.generic import View

from ...models import ReadMessage
from src.core.utils.permissions import OwnerRequiredMixin


class AccountMessagesDeleteManyView(
    OwnerRequiredMixin,
    View
):
    def post(self, *args, **kwargs):
        ids = list(map(lambda x: int(x), self.request.POST.getlist('selected_ids[]')))
        read_messages = [ReadMessage(user_id=self.request.user.id, message_id=message_id) for message_id in ids]
        ReadMessage.objects.bulk_create(read_messages)
        return JsonResponse({'success': True})