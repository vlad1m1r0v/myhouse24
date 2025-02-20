from django.views.generic import DetailView

from .mixin import (
    MasterCallRequestPermissionRequiredMixin,
    HouseUserRequiredMixin
)
from ...models import MasterCallRequest


class AdminMasterCallRequestsDetailView(
    HouseUserRequiredMixin,
    MasterCallRequestPermissionRequiredMixin,
    DetailView
):
    model = MasterCallRequest
    template_name = 'master_call_requests/adminlte/detail.html'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'flat',
            'flat__house',
            'flat_owner',
            'master_type',
            'master',
        ).prefetch_related(
            'master__groups'
        )
