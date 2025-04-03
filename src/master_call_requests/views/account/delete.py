from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from src.core.utils.permissions import OwnerRequiredMixin
from src.master_call_requests.models import MasterCallRequest


class AccountMasterCallRequestDeleteView(
    OwnerRequiredMixin,
    SuccessMessageMixin,
    DeleteView
):
    success_url = reverse_lazy('account:master-call-requests:list')
    model = MasterCallRequest
    success_message = 'Заявку виклику майстра успішно видалено'
