from django.http import JsonResponse
from django.views.generic import View

from ...models import Message
from .mixin import MessagePermissionRequiredMixin


class AdminMessagesDeleteManyView(
    MessagePermissionRequiredMixin,
    View
):
    def post(self, *args, **kwargs):
        ids = list(map(lambda x: int(x), self.request.POST.getlist('selected_ids[]')))
        Message.objects.filter(pk__in=ids).delete()
        return JsonResponse({'success': True})
