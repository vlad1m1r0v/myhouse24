from django.views.generic import ListView
from src.core.utils.permissions import OwnerRequiredMixin
from src.master_call_requests.models import MasterCallRequest


class AccountMasterCallRequestsListView(
    OwnerRequiredMixin,
    ListView
):
    template_name = 'master_call_requests/account/list.html'
    model = MasterCallRequest
    context_object_name = 'requests'

    def get_queryset(self):
        return super().get_queryset().filter(flat_owner=self.request.user).select_related('master_type')