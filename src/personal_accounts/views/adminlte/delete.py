from django.http import JsonResponse
from django.views import View

from .mixin import (
    PersonalAccountPermissionRequiredMixin,
    HouseUserRequiredMixin
)

from ...models import PersonalAccount


class AdminPersonalAccountsDeleteView(
    PersonalAccountPermissionRequiredMixin,
    HouseUserRequiredMixin,
    View):
    def delete(self, request, *args, **kwargs):
        PersonalAccount.objects.get(pk=self.kwargs['pk']).delete()
        return JsonResponse(status=200, data={'success': True})
