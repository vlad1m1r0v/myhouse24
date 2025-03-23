from django.http import JsonResponse
from django.views.generic import View

from ...models import Receipt
from .mixin import ReceiptsPermissionRequiredMixin


class AdminReceiptsDeleteManyView(
    ReceiptsPermissionRequiredMixin,
    View
):
    def post(self, *args, **kwargs):
        ids = list(map(lambda x: int(x), self.request.POST.getlist('selected_ids[]')))
        Receipt.objects.filter(pk__in=ids).delete()
        return JsonResponse({'success': True})
